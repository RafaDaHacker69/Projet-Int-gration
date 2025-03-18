import math
import time
from Boules_De_Neiges import Boules_De_Neiges
import pygame
class Bras_Rotatif:

    def __init__(self, alpha, theta, omega0, inverse):
        self.longueur = 40
        self.largeur = 20
        self.theta = theta *-1
        self.alpha = alpha
        self.omega0 = omega0
        self.ferme = False
        self.boule = False
        self.v = 0
        self.t = 0
        self.posx = 0
        self.posy = 0
        self.inverse = inverse
        self.omega = 0
        self.boule_obj = None
        self.frame_counter = 0
        self.last_omega = 0
        if inverse:
            self.theta = self.theta *-1

    def calcul_de_delta_theta(self):
        if self.alpha == 0:
            self.omega = self.omega0
        else:
            self.omega = self.omega0 + (self.alpha * self.t)
        self.last_omega = self.omega
        delta_theta = (((self.omega * self.t) + (0.5 * self.alpha * (self.t ** 2))) * 180) / math.pi  # Calcul de l'angle
        if self.inverse:
            delta_theta = abs(delta_theta)
        else:
            delta_theta = -abs(delta_theta)
        #print(f"theta : {self.theta}")
        return delta_theta

    def activer_rotation(self, keys, touche):
        if keys[touche]:
            self.t += 0.001 # Incrémentation du temps
            if not self.inverse:
                self.theta = self.theta % 360
                self.theta -= self.calcul_de_delta_theta()
            if self.inverse:
                self.theta = self.theta % 360
                self.theta += self.calcul_de_delta_theta()  # Ajustez le facteur ici si nécessaire
        return self.theta

    def tourner_bras(self, rect, screen):
        rec_taille = rect.get_rect()
        rec_centre_x = rec_taille.center[0]
        rec_centre_y = rec_taille.center[1]
        if not self.inverse:
            rect_rotated = pygame.transform.rotate(rect, -abs(self.theta))
            #print(f"theta : {self.theta}")
            #print(f"t : {self.t}")
        if self.inverse:
            rect_rotated = pygame.transform.rotate(rect, self.theta)
        rectangle_rot_taille = rect_rotated.get_rect()
        rectangle_rot_centre_x = rectangle_rot_taille.center[0]
        rectangle_rot_centre_y = rectangle_rot_taille.center[1]
        diff_x = rectangle_rot_centre_x - rec_centre_x
        diff_y = rectangle_rot_centre_y - rec_centre_y
        pos_bras_x = self.posx - diff_x - 30
        pos_bras_y = self.posy - diff_y - 30
        #image_bras = pygame.image.load("IMAGES/BrasOuvert.png").convert_alpha()
        screen.blit(rect_rotated, (pos_bras_x, pos_bras_y))

    def fermer_main(self, keys, touche):
        if keys[touche]:
            self.ferme = True

    def ramasser_boule(self,lim_min, lim_max,screen):
        if self.ferme and not self.boule and lim_min < self.theta < lim_max:
            self.boule_obj = Boules_De_Neiges(10, 10)
            self.boule = True
            print(f"Boule de neige {self.boule}:")
            self.dessiner_cercle_main(screen)

    def arreter_rotation(self):
        self.t = 0
        self.omega = 0

    def ouvrir_main(self):
        if self.boule_obj is not None and self.boule:
            if self.inverse:
                self.boule_obj.theta = (self.theta + 270)
            else :
                self.boule_obj.theta = -abs(self.theta + 90)
            Boules_De_Neiges.lancement_projectile(self.boule_obj)
        self.ferme = False
        self.boule = False

    def creation_bras_main(self,r,g,b):
        rect = pygame.Surface((100, 80), pygame.SRCALPHA)
        #rect.fill("green")
        if not self.inverse:
            pygame.draw.rect(rect, (r, g, b), (45, 30, self.longueur, self.largeur))  # bras
            pygame.draw.rect(rect, (0, 0, 0), (85, 30, 10, 20))  # main
        if self.inverse:
            pygame.draw.rect(rect, (r, g, b), (15, 30, self.longueur, self.largeur))  # bras droite
            pygame.draw.rect(rect, (0, 0, 0), (5, 30, 10, 20)) #main droite
        return rect

    def grossir_boule(self, lim_min, lim_max):
        if self.boule and self.boule_obj and lim_min < self.theta < lim_max and self.ferme and self.boule_obj.r < 34:
            self.frame_counter += 1
            if self.frame_counter > 20:
                self.boule_obj.r += 1
                self.boule_obj.m = self.boule_obj.r ** 2
                self.frame_counter = 0
        #print(f"rayon : {self.boule_obj.r}, masse : {self.boule_obj.m}")

    def dessiner_cercle_main(self, screen):
        if self.boule and self.boule_obj:
            angle_rad = math.radians(self.theta)
            if self.inverse :
                angle_rad = -angle_rad + math.pi
                offset_x = (self.longueur + 0) * math.cos(angle_rad) + 20
                offset_y = (self.longueur + 0) * math.sin(angle_rad) + 10
            else :
                offset_x = (self.longueur + 0) * math.cos(angle_rad) + 20
                offset_y = (self.longueur + 0) * math.sin(angle_rad) + 10
            circle_x = self.posx + offset_x
            circle_y = self.posy + offset_y
            self.boule_obj.x = circle_x
            self.boule_obj.y = circle_y
            self.boule_obj.vitesse = (self.last_omega * self.longueur)/2 #Vitesse tangeantielle est égale au rayon * vitesse angulaire
            pygame.draw.circle(screen, (173, 216, 230), (circle_x, circle_y), self.boule_obj.r)
            #print(f"x : {circle_x}, y : {circle_y}")

    def mise_a_jour_last_speed(self):
        if not self.boule_obj.lance:
            self.frame_counter +=1
            if self.frame_counter >= 35:
                self.last_omega = 0