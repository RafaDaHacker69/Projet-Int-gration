import math
from Boules_De_Neiges import Boules_De_Neiges
import pygame
class Bras_Rotatif:

    def __init__(self, alpha, theta, omega0, v, inverse):
        self.longueur = 40
        self.largeur = 20
        self.theta = theta *-1
        self.alpha = alpha
        self.omega0 = omega0
        self.ferme = False
        self.boule = False
        self.v = v
        self.t = 0
        self.posx = 0
        self.posy = 0
        self.inverse = inverse
        self.omega = 0
        self.boule_obj = None
        self.frame_counter = 0
        if inverse:
            self.theta = self.theta *-1

    def calcul_de_vitesse_angulaire(self):
        self.omega = self.omega0 + (self.alpha * self.t)
        self.v = self.omega
        if self.inverse:
            self.theta = abs(((self.theta + (self.omega * self.t) + (0.5 * self.alpha * self.t ** 2)) * 180) / math.pi)
            #print(f"theta2  :{self.theta}")
            return self.theta
        elif not self.inverse:
            self.theta = -abs(((self.theta + (self.omega * self.t) + (0.5 * self.alpha * self.t ** 2)) * 180) / math.pi)
            #print(f"theta1  :{self.theta}")
            return self.theta

    def activer_rotation(self,keys,touche):
        if keys[touche]:
            self.t += 0.01
            if not self.inverse:
                self.theta -= self.calcul_de_vitesse_angulaire()*0.0001
                if -abs(self.theta) < -360:
                    self.theta = 0
            if self.inverse:
                self.theta += self.calcul_de_vitesse_angulaire()*0.0001
                if self.theta > 360:
                    self.theta = 0
        return self.theta

    def tourner_bras(self, rect, screen):
        rec_taille = rect.get_rect()
        rec_centre_x = rec_taille.center[0]
        rec_centre_y = rec_taille.center[1]
        if not self.inverse:
            rect_rotated = pygame.transform.rotate(rect, -abs(self.theta))
        if self.inverse:
            rect_rotated = pygame.transform.rotate(rect, self.theta)
        rectangle_rot_taille = rect_rotated.get_rect()
        rectangle_rot_centre_x = rectangle_rot_taille.center[0]
        rectangle_rot_centre_y = rectangle_rot_taille.center[1]
        diff_x = rectangle_rot_centre_x - rec_centre_x
        diff_y = rectangle_rot_centre_y - rec_centre_y
        pos_bras_x = self.posx - diff_x - 30
        pos_bras_y = self.posy - diff_y - 30
        screen.blit(rect_rotated, (pos_bras_x, pos_bras_y))

    def fermer_main(self, keys, touche):
        if keys[touche]:
            self.ferme = True

    def ramasser_boule(self,lim_min, lim_max,screen):
        if self.ferme and not self.boule and self.boule_obj is None and lim_min < self.theta < lim_max:
            self.boule_obj = Boules_De_Neiges(10, 10,0)
            self.boule = True
            print(f"Boule de neige {self.boule}:")
            self.dessiner_cercle_main(screen)

    def arreter_rotation(self):
        self.t = 0
        self.omega = 0
        self.theta = self.theta % 360

    def ouvrir_main(self):
        if self.boule_obj is not None and self.boule:
            self.boule_obj.theta = self.theta + 90
            Boules_De_Neiges.lancement_projectile(self.boule_obj)
        self.ferme = False
        self.boule = False
        self.boule_obj = None

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
        if self.boule and self.boule_obj and lim_min < self.theta < lim_max and self.ferme:
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
                angle_rad = -angle_rad
                offset_x = (self.longueur + 0) * math.cos(angle_rad) + 20
                offset_y = (self.longueur + 0) * math.sin(angle_rad) + 10
            else :
                offset_x = (self.longueur + 0) * math.cos(angle_rad) + 20
                offset_y = (self.longueur + 0) * math.sin(angle_rad) + 10
            circle_x = self.posx + offset_x
            circle_y = self.posy + offset_y
            pygame.draw.circle(screen, (173, 216, 230), (circle_x, circle_y), self.boule_obj.r)