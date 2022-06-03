#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D
from profile import Profile

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
        self.window = glfw.create_window(self.profile.width, self.profile.height, 'Jeu', None, None)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN) #on cache le curseur
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = []
        self.touch = {}

    def run(self):
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.update_key() #On recupere les touches
            if self.profile.get_game_mode() == 0: #Si le jeu est en mode "jeu" 
                self.camera_view(self.profile.get_camera_view_position()) #On uptade la camera en fonction de l'objet

            for obj in self.objs:
                GL.glUseProgram(obj.program)
                if isinstance(obj, Object3D):
                    self.update_camera(obj.program)
                obj.draw()
            

            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
        
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        self.touch[key] = action
    
    def add_object(self, obj):
        self.objs.append(obj)

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

    def camera_view(self, camera_view_position):
        #x,y,z parametre de positionnement de la camera par rapport a l'objet
        x_distance = camera_view_position[0]
        y_distance = camera_view_position[1]
        z_distance = camera_view_position[2]
        self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
        self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi #On met la camera derriere l'objet
        self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center #On met a jour le centre de rotation
        self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([x_distance, y_distance, z_distance]) #On met a jour le placement

    def update_key(self):
        #Rotation
        angle_de_rotation = self.mouse_rotation_step()
        if isinstance(angle_de_rotation, float) :
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += angle_de_rotation*self.profile.get_game_angle_sensibility()

        #Deplacement 
        keys_walk = self.profile.get_game_keys_walk() #For,Back,Left,Right
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
       

    def mouse_rotation_step(self):
        #x,y = 0,0 en bas a gauche
        (x_cursor,y_cursor) = glfw.get_cursor_pos(self.window)
        rapport_de_rotation_largeur = False
        
        if 0<x_cursor<self.profile.width and 0<y_cursor<self.profile.height:
            tour = np.pi*2
            width_screen = self.profile.width

            rapport_de_rotation_largeur = tour*x_cursor/width_screen

            #On centre le rapport:
            rapport_de_rotation_largeur = rapport_de_rotation_largeur-tour/2
        
        glfw.set_cursor_pos(self.window, self.profile.width/2, self.profile.height/2)

        return rapport_de_rotation_largeur



