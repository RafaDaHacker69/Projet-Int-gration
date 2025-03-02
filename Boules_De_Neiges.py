import math


class Boules_De_Neiges:

    def __init__(self, r,m):

        self.r = r #rayon
        self.m = m #masse
        self.theta = 0

    def lancement_projectile(self):
        self.theta = abs(2 * math.pi - (self.theta * math.pi / 180)) #angle en radians
        print(f"Projectile lancé à : {self.theta}")
