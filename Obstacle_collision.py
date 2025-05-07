import pygame

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)  # Create a Pygame rectangle
        self.contact = 0
        self.original_y = y
        self.original_height = height
        self.taille_x = width
        self.taille_y = height

    def draw(self, game_display, color):
        pygame.draw.rect(game_display, color, self.rect)  # Draw the
        # obstacle
    def get_width(self):
        return self.rect.width
    def get_height(self):
        return self.rect.height
    def get_y_pos(self):
        return self.rect.y