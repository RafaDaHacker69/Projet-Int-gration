import pygame


class Bras_Rotatif:

    def __init__(self,r, alpha, theta, m):

        self.y = r  # Hauteur (rayon du bras)
        self.m = m  # Masse en kg
        self.theta = theta
        self.alpha = alpha

    def Calcul_de_vitesse_angulaire(self,omega,t,alpha,theta):
        #t = 0
        #omega = 0
        omega = self.alpha * t
        self.theta = 0.5 * self.alpha * t ** 2
        print(self.theta)
        return self.theta




