from mesh import Mesh
import pyrr
import glutils
from cpe3d import Transformation3D, Object3D
import numpy as np

class Load_Object:
    def __init__(self, mesh='assets/ak47.obj', texture='assets/ak47tr.png', position = [0,2,0], rot_center = 0.2, scale=[1,1,1,1]):
        self.mesh = self.init_mesh(mesh, scale)
        self.transformation = self.init_transformation(position,rot_center)
        self.texture = glutils.load_texture(texture)

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
        viewer.add_object(o)