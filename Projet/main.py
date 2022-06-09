from load_object import Arme, Cible
from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr

def main():
    viewer = ViewerGL()

    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 2
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')

    ak47 = Arme(mesh='assets/AK47.obj', texture='assets/Solid_white_hd.png', position = [0,2,0], rot_center = 0.2, scale=[1,1,1,1])
    ak47.create_add_object(program_id = program3d_id, viewer = viewer)

    viewer.start_game(program3d_id)

    m = Mesh()
    [x1_min, z1_min, x2_max, z2_max] = viewer.get_game_map_size() #taille du sol
    p0, p1, p2, p3 = [x1_min, 0, z1_min], [x2_max, 0, z1_min], [x2_max, 0, z2_max], [z1_min, 0, z2_max]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('assets/sand.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o, None)

    

    vao = Text.initalize_geometry()
    texture = glutils.load_texture('assets/fontB.jpg')
    crosshair_width_12 = viewer.profile.get_game_crosshair_width()/2
    o = Text('+', np.array([-crosshair_width_12,-crosshair_width_12], np.float32), np.array([crosshair_width_12, crosshair_width_12], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o, 'Floor')

    vao = Text.initalize_geometry()
    texture = glutils.load_texture('assets/fontB.jpg')
    o = Text('Timer :', np.array([-1,-1], np.float32), np.array([-1+0.3,-1+0.1], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o, 'Timer')

    vao = Text.initalize_geometry()
    texture = glutils.load_texture('assets/fontB.jpg')
    o = Text('Score :', np.array([1-0.3,-1], np.float32), np.array([1,-1+0.1], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o, 'Score')

    vao = Text.initalize_geometry()
    texture = glutils.load_texture('assets/fontB.jpg')
    o = Text(' ', np.array([-0.3, 0.0], np.float32), np.array([0.3,0.3], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o, 'Resultat')

    vao = Text.initalize_geometry()
    texture = glutils.load_texture('assets/fontB.jpg')
    o = Text(' ', np.array([-0.5, -0.4], np.float32), np.array([0.5,0.0], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o, 'Rejouer')

    viewer.run()


if __name__ == '__main__':
    main()