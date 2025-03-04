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

    def lancement_projectile(self):
        #print(f"theta : {self.theta}")
        self.theta = math.radians(self.theta) #angle en radians
        self.lance = True
        #print(f"x : {self.x}, y : {self.y}, theta : {self.theta}, vitesse : {self.vitesse}, lance : {self.lance}")
        print("boule de neige lancé")

    def trajectoire_projectile(self,screen):
        if self.lance:
            self.t += 0.1
            self.Vx = self.vitesse * math.cos(self.theta)
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
        elif self.x > width:
            self.x = width
            self.lance = False
        if self.y < 0:
            self.y = 0
            self.lance = False
        elif self.y > 590:
            self.y = 590
            self.lance = False

    def check_collision_boule(self,Player):
        player_pos_x = Player.x_position
        player_pos_y = Player.y_position
        #print(player_pos_x, player_pos_y)
        if player_pos_x <= self.x <= player_pos_x + 30 and player_pos_y <= self.y < player_pos_y + 40:
            print("Collision")
            self.lance = False



