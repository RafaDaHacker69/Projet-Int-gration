import pygame
class Bar:
    def __init__(self, x, y, w, h, max, value, type):
        self.value = value
        self.type = type
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max = max

        self.color1 = "green"
        self.color2 = "red"
        if type == "stamina":
            self.color1 = "yellow"
            self.color2 = "cyan"
        if type == "ult":
            self.color1 = "purple"
            self.color2 = "grey"

    def draw(self, screen):
        ratio = self.value / self.max
        pygame.draw.rect(screen, self.color2, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, self.color1, (self.x, self.y, self.w * ratio, self.h))





