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

    def lancement_projectile(self):
        #print(f"theta : {self.theta}")
        self.theta = math.radians(self.theta) #angle en radians
        self.lance = True
        #print(f"x : {self.x}, y : {self.y}, theta : {self.theta}, vitesse : {self.vitesse}, lance : {self.lance}")

    def trajectoire_projectile(self,screen):
        self.t += 0.1
        Vx = self.vitesse * math.cos(self.theta)
        self.x = self.x + (Vx * self.t)
        Vy = self.vitesse * math.sin(self.theta)
        self.y = self.y - ((Vy * self.t) + (((-9.81) * self.t ** 2) / 2))
        self.limites_projectile(screen)

        pygame.draw.circle(screen, (173, 216, 230), (int(self.x), int(self.y)), self.r)
        #print(f"x : {self.x}, y : {self.y}")


    def limites_projectile(self,screen):
        width = screen.get_width()
        height = screen.get_height()
        if self.x < 0:
            self.x = 0
        elif self.x > width:
            self.x = width
        if self.y > 590:
            self.y = 590
        elif self.y < height:
            self.y = height



