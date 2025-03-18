import math
import pygame

class Boules_De_Neiges:

    def __init__(self, r,m):
        self.r = r #rayon
        self.m = m #masse
        self.vitesse = 0
        self.t = 0
        self.theta = 0
        self.x = 0
        self.y = 0
        self.lance = False
        self.Vx = 0
        self.Vy = 0
        self.collision = False

    def lancement_projectile(self):
        #print(f"theta : {self.theta}")
        self.theta = math.radians(self.theta) #angle en radians
        self.lance = True
        self.collision = False
        #print(f"x : {self.x}, y : {self.y}, theta : {self.theta}, vitesse : {self.vitesse}, lance : {self.lance}")
        print("boule de neige lancé")

    def trajectoire_projectile(self,screen):
        if self.lance:
            self.t += 1
            k = 0.7 # "resistence de l'air"
            self.Vx = self.vitesse * math.cos(self.theta)
            self.Vx = self.Vx * k
            self.x = self.x + (self.Vx * self.t)
            self.Vy = self.vitesse * math.sin(self.theta)
            self.y = self.y - ((self.Vy * self.t) + (((-9.81) * self.t ** 2) / 2))
            self.limites_projectile(screen)

            pygame.draw.circle(screen, (173, 216, 230), (int(self.x), int(self.y)), self.r)
            #print(f"x : {self.x}, y : {self.y}")

    def limites_projectile(self,screen):
        width = screen.get_width()
        if self.x < 0:
            self.x = 0
            self.lance = False
            self.collision = True
        elif self.x > width:
            self.x = width
            self.lance = False
            self.collision = True
        # if self.y < 0:
        #     self.y = 0
        #     self.lance = False
        elif self.y > 590:
            self.y = 590
            self.lance = False
            self.collision = True

    def check_collision_boule(self,Player,screen):
        player_pos_x = Player.x_position
        player_pos_y = Player.y_position
        rayon = self.r - 10
        #print(player_pos_x, player_pos_y)

        #Hitboxes
        #pygame.draw.rect(screen, (255, 0, 0), (player_pos_x,player_pos_y-40,30 + rayon,80 + rayon))

        if player_pos_x <= self.x <= player_pos_x + 30 + rayon and player_pos_y-40 <= self.y < player_pos_y + 80 + rayon and not self.collision :
            print("Collision")
            self.lance = False
            self.collision = True
            Vf = ((self.m*self.Vx)+(80*Player.velocity_x))/(self.m+80)
            Player.velocity_x = Vf




