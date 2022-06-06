import glfw


class Profile:
    def __init__(self):
        #On initialise a la taille du moniteur
        #mon = glfw.get_primary_monitor()
        #print(glfw.get_monitor_workarea(mon)) #Probleme
        
        self.width = 1600
        self.height = 800

        self.game_mode = 0 #On commence en mode de jeu/ 1 = Mode libre (on peut se deplacer sans suivre l'objet etc)/ 2=Pause?
        self.camera_view_position_init = [-0.4,0.5,1.5]
        self.camera_view_position = self.camera_view_position_init[:] #Position de la camera par rapport a l'objet en mode jeu

        self.true_distance_step = 0.1 #Distance de deplacement en mode jeu
        self.false_distance_step = 0.5 #Distance de deplacement en mode libre

        self.game_angle_sensibility = 0.25 #Sensibilité de rotation

        self.game_crosshair_width = 0.05 #Taille du crosshair

        self.game_timer_sec = 60 #en seconde

        self.game_forward_walk = glfw.KEY_E
        self.game_backward_walk = glfw.KEY_D
        self.game_leftward_walk = glfw.KEY_S
        self.game_rightward_walk = glfw.KEY_F
        self.game_jump = glfw.KEY_SPACE
        self.game_shoot = glfw.MOUSE_BUTTON_1

    def get_width_height(self):
        return [self.width, self.height]

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

    def get_game_keys_walk(self):
        #Obtenir les touches de deplacement
        return [self.game_forward_walk, self.game_backward_walk, self.game_leftward_walk, self.game_rightward_walk]

    def get_game_shoot(self):
        return self.game_shoot

    def get_game_angle_sensibility(self):
        return self.game_angle_sensibility

    def get_game_crosshair_width(self):
        return self.game_crosshair_width if self.game_mode == 0 else 0

    def set_game_mode(self, val='other'):
        if val == 'other':
            if self.get_game_mode() == 0:
                self.game_mode = 1
            elif self.get_game_mode() == 1:
                self.game_mode = 0
                self.set_camera_view_position() #On reinitialise la camera
        else:
            self.game_mode = int(val)
        print('Le jeu est à présent en mode',self.get_game_mode())

    def set_camera_view_position(self, val=[0,0,0]):
        if val == [0,0,0]:
            self.camera_view_position = self.camera_view_position_init
        else:
            for i in range(len(val)):
                self.camera_view_position[i] += val[i]

    def get_game_timer_sec(self):
        return self.game_timer_sec