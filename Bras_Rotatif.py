from Boules_De_Neiges import Boules_De_Neiges
import pygame
class Bras_Rotatif:

    def __init__(self, r, alpha, theta, m, omega0, ferme, boule, v, t, posx, posy):

        self.y = r  # Hauteur (rayon du bras)
        self.m = m  # Masse en kg
        self.theta = theta
        self.alpha = alpha
        self.omega0 = omega0
        self.ferme = ferme
        self.boule = boule
        self.v = v
        self.t = t
        self.posx = posx
        self.posy = posy

    def calcul_de_vitesse_angulaire(self, t, omega):
        omega = self.omega0 + self.alpha * self.t
        self.v = omega
        self.theta = self.theta + omega * t + 0.5 * self.alpha * self.t ** 2
        return self.theta

    def activer_rotation(self,keys,touche,i,omega,inverse):
        if keys[touche]:
            self.t += 0.01
            if not inverse:
                i -= self.calcul_de_vitesse_angulaire(self.t, omega)
                if i < -360:
                    i = 0
            if inverse:
                i += self.calcul_de_vitesse_angulaire(self.t, omega)
                if i > 360:
                    i = 0
        return i

    def tourner_bras(self, rect, i, screen,):
        rec_taille = rect.get_rect()
        rec_centre_x = rec_taille.center[0]
        rec_centre_y = rec_taille.center[1]
        rect_rotated = pygame.transform.rotate(rect, i)
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