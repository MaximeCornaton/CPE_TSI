

class Profile:
    def __init__(self):
        self.game_mode = True #On commence en mode de jeu/ False = Mode libre (on peut se deplacer sans suivre l'objet etc)
        self.camera_view_position = [0,1,5] #Position de la camera par rapport a l'objet en mode jeu

        self.true_distance_step = 0.25 #Distance de deplacement en mode jeu
        self.false_distance_step = 0.5 #Distance de deplacement en mode libre

        self.game_angle_step = 0.1 #Angle de rotation
 
    def get_camera_view_position(self):
    #Retourne la position de la camera par rapport a l'objet en mode jeu
        return self.camera_view_position

    def get_game_mode(self):
    #Retourne le mode
        return self.game_mode

    def get_game_distance_step(self): 
    #Retourne la distance de deplacement en fonction du mode
        if self.game_mode == True:
            return self.true_distance_step
        else:
            return self.false_distance_step

    def get_game_angle_step(self):
        return self.game_angle_step