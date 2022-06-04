import time
from mesh import Mesh
import pyrr
import glutils
from cpe3d import Transformation3D, Object3D
import numpy as np

class Load_Object:
    def __init__(self, mesh='assets/ak47.obj', texture='assets/ak47tr.png', position = [0,2,0], rot_center = 0.2, scale=[1,1,1,1], weight = 5, ymin = 2):
        self.weight = weight
        self.ymin = ymin

        self.mesh = self.init_mesh(mesh, scale)
        self.transformation = self.init_transformation(position,rot_center)
        self.texture = glutils.load_texture(texture)

        self.object = None
        self.viewer = None
        self.program_id = None

    def init_mesh(self, mesh, scale=[1,1,1,1]):
        mesh = Mesh.load_obj(mesh)
        mesh.normalize()
        mesh.apply_matrix(pyrr.matrix44.create_from_scale(scale)) 
        return mesh
    
    def init_transformation(self, position, rot_center):
        tr = Transformation3D() #Position initiale de l'objet
        tr.translation.y = -np.amin(self.mesh.vertices, axis=0)[1] 
        tr.translation.x += position[0]
        tr.translation.y += position[1]
        tr.translation.z += position[2]
        tr.rotation_center.z = rot_center 
        return tr
        
    def get_mesh(self):
        return self.mesh

    def get_transformation(self):
        return self.transformation

    def get_texture(self):
        return self.texture

    def create_add_object(self, program_id, viewer):
        o = Object3D(self.mesh.load_to_gpu(), self.mesh.get_nb_triangles(), program_id, self.texture, self.transformation)
        viewer.add_object(o, self)
        self.object = o
        self.viewer = viewer
        self.program_id = program_id
        return o

    def get_position(self):
        return self.object.transformation.translation

    def gravity(self):
        #print(self.transformation.translation[1], self.ymin)
        if self.transformation.translation[1] > self.ymin:
            self.transformation.translation[1] -= self.weight*(self.transformation.translation[1]-self.ymin)/10
        if self.transformation.translation[1] < self.ymin:
            self.transformation.translation[1] = self.ymin


class Bullet(Load_Object):
    def __init__(self, mesh, texture, position, rot_center, scale, bullet_speed = 0.1, weight = 0):
        super().__init__(mesh, texture, position, rot_center, scale, weight)
        self.bullet_speed = bullet_speed #vitesse des balles
        self.bullet_weight = weight
        
    def auto_movement(self, objs):
        [x,y,z] = self.get_position()

        #objs[1].transformation.translation
        [x_lim,z_lim] = 10,10 #taille du sol
        rotation = objs[0].transformation.rotation_euler

        vecteur_translation = pyrr.Vector3([0, 0, self.bullet_speed])
        self.object.transformation.rotation_euler[pyrr.euler.index().yaw] += rotation[2]
        
        while(-x_lim<x<x_lim and -z_lim<z<z_lim):
            
            self.object.transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.object.transformation.rotation_euler), vecteur_translation)
            [x,y,z] = self.get_position()

class Arme(Load_Object):
    def __init__(self, mesh, texture, position, rot_center, scale, freq_tire = 3, weight = 5):
        super().__init__(mesh, texture, position, rot_center, scale, weight)
        self.freq_tire = freq_tire #frequence de tir par seconde
        self.weight = weight

        self.last_shoot = 0

        self.bullet = []

    def shoot(self, objs):
        time_now = time.time()
        if (time_now-self.last_shoot > 1/self.freq_tire):
            self.last_shoot = time_now
            position_bullet = self.object.transformation.translation #Position de l'arme
            bullet = Bullet(mesh='assets/bullet2.obj', texture='assets/ak47tr.png', position = position_bullet, rot_center = 0.0, scale=[0.1,0.1,0.1,1])
            self.bullet.append(bullet)
            self.bullet[-1].create_add_object(program_id = self.program_id, viewer = self.viewer)
            self.bullet[-1].auto_movement(objs)

    def jump(self):
        print('jump')