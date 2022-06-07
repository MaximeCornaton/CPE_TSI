#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D
from profile import Profile
import time

from load_object import Bullet, Cible

class ViewerGL:
    def __init__(self):
        #Initialisation du profil joueur
        self.profile = Profile()

        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        [width, height] = self.profile.get_width_height()
        self.window = glfw.create_window(width, height, 'Jeu', None, None)
        glfw.set_window_pos(self.window, 50,50)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN) #on cache le curseur
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_callback)
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = []
        self.objects = []
        self.touch = {}

        self.animation = False
        self.timer = time.time()
        self.score = 0


    def run(self):
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.update_key() #On recupere les touches
            if self.animation == False: #Si on est pas en pleine animation
                self.camera_view() #On uptade la camera en fonction de l'objet

            
            if self.profile.get_game() == True:
                i = self.objects.index('Resultat')
                self.objs[i].value = ' '
                self.objs[i].draw()
                i = self.objects.index('Rejouer')
                self.objs[i].value = ' '
                for i,obj in enumerate(self.objs):
                    GL.glUseProgram(obj.program)
                    if isinstance(obj, Object3D):
                        self.update_camera(obj.program)
                    if self.objects[i] != None and isinstance(self.objects[i], str) == False:
                        self.objects[i].gravity()
                    if self.objects[i] == 'Timer':
                        obj.value = 'Timer : '+str(self.get_timer())
                    if self.objects[i] == 'Score':
                        obj.value = 'Score : '+str(self.score)
                    obj.draw()
            else: 
                i = self.objects.index('Resultat')
                self.objs[i].value = 'Score : '+str(self.score)
                self.objs[i].draw()
                i = self.objects.index('Rejouer')
                self.objs[i].value = 'Entree pour Rejouer'
                self.objs[i].draw()

            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
        
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        self.touch[key] = action
        #Mode libre
        if glfw.KEY_C in self.touch and self.touch[glfw.KEY_C] > 0 and glfw.KEY_V in self.touch and self.touch[glfw.KEY_V] > 0:
            self.profile.set_game_mode()
        #Rejouer
        if glfw.KEY_ENTER in self.touch and self.touch[glfw.KEY_ENTER] > 0 and self.profile.get_game() == False:
            self.start_game(self.program_id)

    def mouse_callback(self,win, button, action, mods):
        self.touch[button] = action
    
    def add_object(self, obj, objects):
        self.objs.append(obj)
        self.objects.append(objects)

    def set_camera(self, cam):
        self.cam = cam

    def update_camera(self, prog):
        GL.glUseProgram(prog)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
    
        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1) :
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)

    def camera_view(self):
        #x,y,z parametre de positionnement de la camera par rapport a l'objet
        [x_distance, y_distance, z_distance] = self.profile.get_camera_view_position()
        self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
        self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi #On met la camera derriere l'objet
        #self.cam.transformation.rotation_euler[pyrr.euler.index().roll] = -self.cam.transformation.rotation_euler[pyrr.euler.index().roll]
        self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center #On met a jour le centre de rotation
        self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([x_distance, y_distance, z_distance]) #On met a jour le placement

    def update_key(self):
        keys_walk = self.profile.get_game_keys_walk() #For,Back,Left,Right

        if self.profile.get_game_mode() == 0:
            #Rotation
            [angle_de_rotation_y,angle_de_rotation_x] = self.mouse_rotation_step()
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += angle_de_rotation_y*self.profile.get_game_angle_sensibility()
            #self.objs[0].transformation.rotation_euler[pyrr.euler.index().roll] += angle_de_rotation_x*self.profile.get_game_angle_sensibility()/2

            #Deplacement 
            if keys_walk[0] in self.touch and self.touch[keys_walk[0]] > 0:
                self.objs[0].transformation.translation += \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, self.profile.get_game_distance_step()]))
            if keys_walk[1] in self.touch and self.touch[keys_walk[1]] > 0:
                self.objs[0].transformation.translation -= \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, self.profile.get_game_distance_step()]))
            if keys_walk[2] in self.touch and self.touch[keys_walk[2]] > 0:
                self.objs[0].transformation.translation += \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([self.profile.get_game_distance_step(), 0, 0]))
            if keys_walk[3] in self.touch and self.touch[keys_walk[3]] > 0:
                self.objs[0].transformation.translation -= \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([self.profile.get_game_distance_step(), 0, 0]))
            

            #Tir
            if self.profile.get_game_shoot() in self.touch and self.touch[self.profile.get_game_shoot()] > 0:
                self.objects[0].shoot(self.objs, self.objects, size_map= self.profile.get_game_size_map())

        elif self.profile.get_game_mode() == 1:
            if keys_walk[0] in self.touch and self.touch[keys_walk[0]] > 0:
               self.profile.set_camera_view_position(val=[0,0,-1])
            if keys_walk[1] in self.touch and self.touch[keys_walk[1]] > 0:
                self.profile.set_camera_view_position(val=[0,0,1])
            if keys_walk[2] in self.touch and self.touch[keys_walk[2]] > 0:
                self.profile.set_camera_view_position(val=[-1,0,0])
            if keys_walk[3] in self.touch and self.touch[keys_walk[3]] > 0:
                self.profile.set_camera_view_position(val=[1,0,0])

    def mouse_rotation_step(self):
        #x,y = 0,0 en bas a gauche
        (x_cursor,y_cursor) = glfw.get_cursor_pos(self.window)
        rapport_de_rotation_largeur = 0
        rapport_de_rotation_hauteur = 0

        [width, height] = self.profile.get_width_height()
        
        if 0<x_cursor<width and 0<y_cursor<height:
            tour = np.pi*2

            rapport_de_rotation_largeur = tour*x_cursor/width
            rapport_de_rotation_hauteur = tour*y_cursor/height

            #On centre le rapport:
            rapport_de_rotation_largeur = rapport_de_rotation_largeur-tour/2
            rapport_de_rotation_hauteur = rapport_de_rotation_hauteur-tour/2
        
        glfw.set_cursor_pos(self.window, width/2, height/2)
        return rapport_de_rotation_largeur, -rapport_de_rotation_hauteur


    def set_program_id(self, program3d_id):
        self.program_id = program3d_id

    def get_timer(self):
        time_ = time.time()
        if int(time_-self.timer) < self.profile.get_game_timer_sec():
            return int(time_-self.timer)
        else: 
            self.profile.set_game(False)

    def add_score(self, i):
        self.score += i

    def set_score(self, i=0):
        self.score = i

    def get_game_map_size(self):
        return self.profile.get_game_size_map()

    def set_timer(self, val = ''):
        self.timer = val if val != '' else time.time()


    def start_game(self, program3d_id):
        self.set_program_id(program3d_id)
        self.set_timer()
        self.profile.set_game(True)
        self.set_score()
        cible = Cible(mesh='assets/target.obj', texture='assets/textB1!.png', position = [0,0,10], rot_center = 0.2, scale=[1,1,1,1], rotation=[0,0,np.pi])
        cible.create_add_object(program_id = program3d_id, viewer = self)