
class Boules_De_Neiges:

    def __init__(self, r,m,theta):

        self.r = r #rayon
        self.m = m #masse
        self.theta = 0

    def lancement_projectile(self):
        print(f"Projectile lancé à : {self.theta}")
