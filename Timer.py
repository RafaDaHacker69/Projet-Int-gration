import pygame
import sys

class Timer:
    def __init__(self,secs,taille,x,y,couleur,screen):
        self.secs = secs
        self.x = x
        self.y = y
        self.couleur = couleur
        self.temps=secs
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.font = pygame.font.Font("IMAGES/grand9k-pixel.ttf", taille)
        self.tick0 = pygame.time.get_ticks()
        self.fini=False

    def update(self):
        if not self.fini:
            self.tempsPasse = (pygame.time.get_ticks() - self.tick0) // 1000
            self.temps = max(self.secs - self.tempsPasse, 0)

            if self.temps == 0:
                self.fini = True

    def draw(self):
        minutes = self.temps // 60
        seconds = self.temps % 60
        timer_text = f"{minutes:02}:{seconds:02}"

        text_surface = self.font.render(timer_text, True, self.couleur)
        self.screen.blit(text_surface, (self.x, self.y))

    def reset(self):
        self.tick0 = pygame.time.get_ticks()
        self.temps = self.secs
        self.fini = False

    def is_finished(self):
        return self.fini

    def getTemps(self):
        if (self.fini):
            return 0
        return (pygame.time.get_ticks() - self.tick0) // 1000


