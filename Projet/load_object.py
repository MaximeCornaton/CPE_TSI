import time
from mesh import Mesh
import pyrr
import glutils
from cpe3d import Transformation3D, Object3D
import numpy as np

class Load_Object:
    def __init__(self, mesh='assets/icosphere.obj', texture='assets/Solid_white_hd.png', position = [0,2,0], rot_center = 0.2, scale=[1,1,1,1], weight = 5, ymin = 2,rotation = [0,0,0],):
        self.weight = weight
        self.ymin = ymin

        self.mesh = self.init_mesh(mesh, scale)
        self.transformation = self.init_transformation(position,rot_center, rotation)
        self.texture = glutils.load_texture(texture)
        
        self.object = None
        self.viewer = None
        self.program_id = None

    def init_mesh(self, mesh, scale=[1,1,1,1]):
        mesh = Mesh.load_obj(mesh)
        mesh.normalize()
        mesh.apply_matrix(pyrr.matrix44.create_from_scale(scale)) 
        return mesh
    
    def init_transformation(self, position, rot_center, rotation):
        tr = Transformation3D() #Position initiale de l'objet
        tr.translation.x += position[0]
        tr.translation.y += position[1]
        tr.translation.z += position[2]
        tr.rotation_euler[0] += rotation[0]
        tr.rotation_euler[1] += rotation[1]
        tr.rotation_euler[2] += rotation[2]
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

    def centre_gravite(self):
        [x,y,z] = self.get_position()
        return [x,y,z]

    def remove_(self, objs, objs_global):
        objs.remove(self.object)
        objs_global.remove(self)

    def new_cible_random(self, size_map, program3d_id, viewer):
        [x1_min, z1_min, x2_max, z2_max] = size_map#taille du sol

        x = np.random.randint(x1_min,x2_max)
        z = np.random.randint(z1_min,z2_max)

        cible = Cible(mesh='assets/target.obj', texture='assets/textB1!.png', position = [x,0,z], rot_center = 0.2, scale=[1,1,1,1], rotation=[0,0,np.pi])
        cible.create_add_object(program_id = program3d_id, viewer = viewer)

class Bullet(Load_Object):
    def __init__(self, mesh, texture, position, rot_center, scale, bullet_speed = 0.1, weight = 0, ymin = 2, rotation=[0,0,0]):
        super().__init__(mesh, texture, position, rot_center, scale, weight, ymin, rotation)
        self.bullet_speed = bullet_speed #vitesse des balles
        self.bullet_weight = weight

        self.transformation.translation.y += 0.5
        
    def auto_movement(self, objs, objs_global, size_map):
        #self.transformation.translation.x += 0.4
        #self.transformation.translation.z -= 1.5
        [x,y,z] = self.get_position()
        collision = False

        #objs[1].transformation.translation
        [x1_min, z1_min, x2_max, z2_max] = size_map #taille du sol
        rotation = objs[0].transformation.rotation_euler

        vecteur_translation = pyrr.Vector3([0, 0, self.bullet_speed])
        self.object.transformation.rotation_euler[pyrr.euler.index().yaw] += rotation[2]
        self.object.transformation.rotation_euler[pyrr.euler.index().roll] += rotation[0]
        
        while(-5<x<5 and -5<z<5 and collision == False):
            self.object.transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.object.transformation.rotation_euler), vecteur_translation)
            for obj in objs_global:
                if type(obj) == Cible:
                    dist_euclidienne = np.linalg.norm(self.get_position()-obj.get_position())
                    if dist_euclidienne < 1:
                        obj.hit(objs, objs_global) #On renvoie vers la fonction de touchage de cible
                        self.remove_(objs, objs_global) #Supprime la balle
                        collision = True #on arrete le deplacement
                        self.new_cible_random(size_map, self.program_id, self.viewer)
            [x,y,z] = self.get_position()

class Arme(Load_Object):
    def __init__(self, mesh, texture, position, rot_center, scale, freq_tire = 3, weight = 5, ymin = 2, rotation=[0,0,0]):
        super().__init__(mesh, texture, position, rot_center, scale, weight, ymin, rotation)
        self.freq_tire = freq_tire #frequence de tir par seconde
        self.weight = weight

        self.last_shoot = 0

        self.bullet = []

    def shoot(self, objs,objects, size_map):
        time_now = time.time()
        if (time_now-self.last_shoot > 1/self.freq_tire):
            self.last_shoot = time_now
            position_bullet = self.object.transformation.translation #Position de l'arme
            bullet = Bullet(mesh='assets/icosphere.obj', texture='assets/Solid_white_hd.png', position = position_bullet, rot_center = 0.0, scale=[0.02,0.02,0.02,1])
            self.bullet.append(bullet)
            self.bullet[-1].create_add_object(program_id = self.program_id, viewer = self.viewer)
            self.bullet[-1].auto_movement(objs,objects, size_map)

    def jump(self):
        print('jump')

class Cible(Load_Object):
    def __init__(self, mesh, texture, position, rot_center, scale, weight = 10, ymin = 2, rotation=[0,0,0]):
        super().__init__(mesh, texture, position, rot_center, scale, weight,ymin, rotation)

    def hit(self, objs, objs_global):
        self.remove_(objs, objs_global)
        self.viewer.add_score(1)
    