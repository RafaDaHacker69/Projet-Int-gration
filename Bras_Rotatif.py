import math

from Boules_De_Neiges import Boules_De_Neiges
import pygame
class Bras_Rotatif:

    def __init__(self, r, alpha, theta, m, omega0, ferme, boule, v, t, posx, posy, inverse, omega):
        self.y = r  # Hauteur (rayon du bras)
        self.m = m  # Masse en kg
        self.theta = theta *-1
        self.alpha = alpha
        self.omega0 = omega0
        self.ferme = ferme
        self.boule = boule
        self.v = v
        self.t = t
        self.posx = posx
        self.posy = posy
        self.inverse = inverse
        self.omega = omega
        if inverse:
            self.theta = self.theta *-1

    def calcul_de_vitesse_angulaire(self):
        self.omega = self.omega0 + self.alpha * self.t
        self.v = self.omega
        if self.inverse:
            self.theta = abs(((self.theta + self.omega * self.t + 0.5 * self.alpha * self.t ** 2) * 180) / math.pi)
            print(f"theta2  :{self.theta}")
            return self.theta
        elif not self.inverse:
            self.theta = -abs(((self.theta + self.omega * self.t + 0.5 * self.alpha * self.t ** 2) * 180) / math.pi)
            print(f"theta1  :{self.theta}")
            return self.theta


    def activer_rotation(self,keys,touche):
        if keys[touche]:
            self.t += 0.01
            if not self.inverse:
                self.theta -= self.calcul_de_vitesse_angulaire()*0.0001
                # if -abs(self.theta) < -360:
                #     self.theta = 0
            if self.inverse:
                self.theta += self.calcul_de_vitesse_angulaire()*0.0001
                # if self.theta > 360:
                #     self.theta = 0
        return self.theta

    def tourner_bras(self, rect,screen):
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
        screen.blit(rect_rotated, (self.posx - diff_x - 30, self.posy - diff_y - 30))

    def fermer_main(self, keys, touche):
        if keys[touche]:
            self.ferme = True

    def ramasser_boule(self, i, lim_min, lim_max):
        if self.ferme and not self.boule and lim_min < i < lim_max:
            boule = Boules_De_Neiges(0.01, 0.01)
            self.boule = True
            print(f"Boule de neige {self.boule}:")