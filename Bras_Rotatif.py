


class Bras_Rotatif:

    def __init__(self,r, alpha, theta, m, omega0, ferme, boule,v):

        self.y = r  # Hauteur (rayon du bras)
        self.m = m  # Masse en kg
        self.theta = theta
        self.alpha = alpha
        self.omega0 = omega0
        self.ferme = ferme
        self.boule = boule
        self.v = v

    def calcul_de_vitesse_angulaire(self, t, omega):
        omega = self.omega0 + self.alpha * t
        self.v = omega
        self.theta = self.theta + omega * t + 0.5 * self.alpha * t ** 2
        return self.theta




