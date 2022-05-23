#!/usr/bin/env python3

import os
import OpenGL.GL as GL
import glfw
import numpy as np
import random as rdm
import pyrr

keys_ = {}

def compile_shader(shader_content, shader_type):
    # compilation d'un shader donné selon son type
    shader_id = GL.glCreateShader(shader_type)
    GL.glShaderSource(shader_id, shader_content)
    GL.glCompileShader(shader_id)
    success = GL.glGetShaderiv(shader_id, GL.GL_COMPILE_STATUS)
    if not success:
        log = GL.glGetShaderInfoLog(shader_id).decode('ascii')
        print(f'{25*"-"}\nError compiling shader: \n\
            {shader_content}\n{5*"-"}\n{log}\n{25*"-"}')
    return shader_id

def create_program( vertex_source, fragment_source):
    # creation d'un programme gpu
    vs_id = compile_shader(vertex_source, GL.GL_VERTEX_SHADER)
    fs_id = compile_shader(fragment_source, GL.GL_FRAGMENT_SHADER)
    if vs_id and fs_id:
        program_id = GL.glCreateProgram()
        GL.glAttachShader(program_id, vs_id)
        GL.glAttachShader(program_id, fs_id)
        GL.glLinkProgram(program_id)
        success = GL.glGetProgramiv(program_id, GL.GL_LINK_STATUS)
        if not success:
            log = GL.glGetProgramInfoLog(program_id).decode('ascii')
            print(f'{25*"-"}\nError linking program:\n{log}\n{25*"-"}')
        GL.glDeleteShader(vs_id)
        GL.glDeleteShader(fs_id)
    return program_id

def create_program_from_file(vs_file, fs_file):
    # creation d'un programme gpu à partir de fichiers
    vs_content = open(vs_file, 'r').read() if os.path.exists(vs_file)\
    else print(f'{25*"-"}\nError reading file:\n{vs_file}\n{25*"-"}')
    fs_content = open(fs_file, 'r').read() if os.path.exists(fs_file)\
    else print(f'{25*"-"}\nError reading file:\n{fs_file}\n{25*"-"}')
    return create_program(vs_content, fs_content)

def init_window():
    # initialisation de la librairie glfw
    glfw.init()
    # parametrage du context opengl
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    # creation et parametrage de la fenetre
    glfw.window_hint(glfw.RESIZABLE, False)
    window = glfw.create_window(800, 800, 'OpenGL', None, None)
    # parametrage de la fonction de gestion des evenements
    glfw.set_key_callback(window, key_callback)
    return window

def init_context(window):
    # activation du context OpenGL pour la fenetre
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    # activation de la gestion de la profondeur
    GL.glEnable(GL.GL_DEPTH_TEST)
    # choix de la couleur de fond
    GL.glClearColor(0.1, 0.9, 0.1, 1.0)
    print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

def init_program():
    shader_id = create_program_from_file('shader.vert','shader.frag')
    GL.glUseProgram(shader_id)

        
def init_data():
    sommets = np.array(((0, 0, 0), (1, 0, 0), (0, 1, 0)), np.float32)
    
    # attribution d'une liste d'état (1 indique la création d'une seule liste)
    vao = GL.glGenVertexArrays(1)
    # affectation de la liste d'état courante
    GL.glBindVertexArray(vao)
    # attribution d’un buffer de donnees (1 indique la création d’un seul buffer)
    vbo = GL.glGenBuffers(1)
    # affectation du buffer courant
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)

    # copie des donnees des sommets sur la carte graphique
    GL.glBufferData(GL.GL_ARRAY_BUFFER, sommets, GL.GL_STATIC_DRAW)

    # Les deux commandes suivantes sont stockées dans l'état du vao courant
    # Active l'utilisation des données de positions
    # (le 0 correspond à la location dans le vertex shader)
    GL.glEnableVertexAttribArray(0)
    # Indique comment le buffer courant (dernier vbo "bindé")
    # est utilisé pour les positions des sommets
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)


def run(window):
    ### INITIALISATION 
    for i in range(glfw.KEY_LAST):
        keys_[i] = 0

    x=0
    y=0

    r=0
    g=0
    b=0

    angx = 0
    angy = 0

    angproj = 50
    distproj = 5

    # boucle d'affichage
    while not glfw.window_should_close(window):
        # nettoyage de la fenetre : fond et profondeur
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        #  l'affichage se fera ici
        """ if glfw.get_time() < 1:
            GL.glClearColor(glfw.get_time(), glfw.get_time(), glfw.get_time(), 1.0)
        """
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        #GL.glPointSize(5.0) 
        #GL.glDrawArrays(GL.GL_POINTS, 0, 3)
        #GL.glDrawArrays(GL.GL_LINE_LOOP, 0, 3)

        # Récupère l'identifiant du programme courant
        prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)

        # Récupère l'identifiant de la variable translation/couleur dans le programme courant
        loc = GL.glGetUniformLocation(prog, "translation")
        loc_color = GL.glGetUniformLocation(prog, "c")
        loc_rotation = GL.glGetUniformLocation(prog, "rotation")
        loc_projection = GL.glGetUniformLocation(prog, "projection")

        # Vérifie que les variables existent
        if loc == -1 :
            print("Pas de variable uniforme : translation")
        if loc_color == -1 :
            print("Pas de variable uniforme : c")
        if loc_rotation == -1 :
            print("Pas de variable uniforme : rotation")
        if loc_projection == -1 :
            print("Pas de variable uniforme : projection")

        #Appliquer les parametres
        if keys_[glfw.KEY_RIGHT] > 0:
            x += 0.05
        if keys_[glfw.KEY_LEFT] > 0:
            x -= 0.05
        if keys_[glfw.KEY_UP] > 0:
            y += 0.05
        if keys_[glfw.KEY_DOWN] > 0:
            y -= 0.05

        if keys_[glfw.KEY_I] > 0:
            angx += 0.05*(np.pi)
        if keys_[glfw.KEY_J] > 0:
            angx -= 0.05*(np.pi)
        if keys_[glfw.KEY_K] > 0:
            angy += 0.05*(np.pi)
        if keys_[glfw.KEY_L] > 0:
            angy -= 0.05*(np.pi)
        
        rotx3 = pyrr.matrix33.create_from_x_rotation(angx) 
        roty3 = pyrr.matrix33.create_from_y_rotation(angy)
        rotx4 = pyrr.matrix44.create_from_matrix33(rotx3)
        roty4 = pyrr.matrix44.create_from_matrix33(roty3)

        if keys_[glfw.KEY_R] > 0:
            r = 1
            g=0
            b=0
        if keys_[glfw.KEY_G] > 0:
            r = 0
            g = 1
            b = 0
        if keys_[glfw.KEY_B] > 0:
            r = 0
            g = 0
            b = 1
        
        if keys_[glfw.KEY_Y] > 0:
            distproj = 0.5
        if keys_[glfw.KEY_H] > 0:
            distproj = 10
            
        # Mise a jour des positions et couleurs
        GL.glUniform4f(loc, x, y, 0, 0)
        GL.glUniform4f(loc_color, r, g, b, 0)
        GL.glUniformMatrix4fv(loc_rotation, 1, GL.GL_FALSE, rotx4+roty4)
        

        matproj4 = pyrr.matrix44.create_perspective_projection_matrix(50.0,1.0,0.5,10.0, None)
        GL.glUniformMatrix4fv(loc_projection, 1, GL.GL_FALSE, matproj4)
    

        # changement de buffer d'affichage pour eviter un effet de scintillement
        glfw.swap_buffers(window)
        # gestion des evenements
        glfw.poll_events()

def key_callback(win, key, scancode, action, mods):

    keys_[key] = action

    # sortie du programme si appui sur la touche 'echap'
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(win, glfw.TRUE)

def main():
    window = init_window()
    init_context(window)
    init_program()
    init_data()
    run(window)
    glfw.terminate()


if __name__ == '__main__':
    main()