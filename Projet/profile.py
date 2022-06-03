import glfw


class Profile:
    def __init__(self):
        #On initialise a la taille du moniteur
        mon = glfw.get_primary_monitor()
        print(glfw.get_monitor_workarea(mon)) #Probleme
        
        self.width = 1200
        self.height = 800

        self.game_mode = 0 #On commence en mode de jeu/ 1 = Mode libre (on peut se deplacer sans suivre l'objet etc)/ 2=Pause?
        self.camera_view_position = [0,1,2] #Position de la camera par rapport a l'objet en mode jeu

        self.true_distance_step = 0.15 #Distance de deplacement en mode jeu
        self.false_distance_step = 0.5 #Distance de deplacement en mode libre

        self.game_angle_sensibility = 0.5 #Sensibilité de rotation

        self.game_forward_walk = glfw.KEY_E
        self.game_backward_walk = glfw.KEY_D
        self.game_leftward_walk = glfw.KEY_S
        self.game_rightward_walk = glfw.KEY_F

    def get_camera_view_position(self):
    #Retourne la position de la camera par rapport a l'objet en mode jeu
        return self.camera_view_position

    def get_game_mode(self):
    #Retourne le mode
        return self.game_mode

    def get_game_distance_step(self): 
    #Retourne la distance de deplacement en fonction du mode
        if self.game_mode == 0:
            return self.true_distance_step
        else:
            return self.false_distance_step

    def get_game_angle_step(self):
        return self.game_angle_step

    def get_game_keys_walk(self):
        #Obtenir les touches de deplacement
        return [self.game_forward_walk, self.game_backward_walk, self.game_leftward_walk, self.game_rightward_walk]

    def get_game_angle_sensibility(self):
        return self.game_angle_sensibility