import math
import pygame
import time

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
        self.hitboxe = None
        self.dmg = 0

    def lancement_projectile(self):
        self.theta = math.radians(self.theta) #angle en radians
        self.lance = True
        self.collision = False
        print("boule de neige lancé")

    def trajectoire_projectile(self,screen):
        gravite = -150
        if self.lance:
            self.t += 1/60
            self.Vx = self.vitesse * math.cos(self.theta)
            self.x = self.x + (self.Vx * self.t)
            self.Vy = self.vitesse * math.sin(self.theta)
            self.y = self.y - (self.Vy * self.t + (gravite) * self.t ** 2)
            self.limites_projectile(screen)

            pygame.draw.circle(screen, (173, 216, 230), (int(self.x), int(self.y)), self.r)
            print(f"x : {self.x}, y : {self.y}")

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
        elif self.y > 590:
            self.y = 590
            self.lance = False
            self.collision = True

    def check_collision_boule(self,player,screen,menu_de_mort):
        rayon = self.r
        self.hitboxe = pygame.Rect(self.x-rayon,self.y-rayon, rayon*2, rayon*2)

        #Dessin de la hitboxe de la boule
        #pygame.draw.rect(screen, (255, 0, 0), self.hitboxe, 2)

        if self.hitboxe.colliderect(player.hitboxe) and self.lance:
            self.collision = True
            self.lance = False
            vf = ((self.m * self.Vx) + (80 * player.vitesse_x)) / (self.m + 80)
            player.vitesse_x = vf
            modVit=math.sqrt(self.Vx**2 + self.Vy**2)
            self.dmg = self.m*modVit/(80*15)
            self.degat_inflige(player,menu_de_mort)
            print(f"VF :{vf}")

    def degat_inflige(self,player,menu_de_mort):
        player.pv -= self.dmg
        self.dmg = 0
        print(f"Pv : {player.pv}")
        if player.pv < 0:
            print("Le joueur est mort")
            menu_de_mort.menu_mort()






