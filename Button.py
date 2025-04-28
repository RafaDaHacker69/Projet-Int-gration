import pygame

class Button:
    def __init__(self, position, text, scale=1.0, prop=1.2, font_size=20, font_color=(255, 255, 255)):
        self.original_image = pygame.image.load("IMAGES/Button.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=position)
        self.scale = scale
        self.prop = prop
        self.hovered = False
        self.text = text
        self.base_font_size = font_size

        pygame.font.init()
        self.font = pygame.font.Font("IMAGES/grand9k-pixel.ttf", font_size)
        self.font_color = font_color
        self.update_text_surface(font_size)

    def update_text_surface(self, font_size):
        self.font = pygame.font.Font("IMAGES/grand9k-pixel.ttf", font_size)
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def verifier(self, mouse_pos):  # Vérifier si la souris est au-dessus du bouton
        if self.rect.collidepoint(mouse_pos):
            if not self.hovered:
                self.image = pygame.transform.scale(
                    self.original_image,
                    (int(self.original_image.get_width() * self.prop),
                     int(self.original_image.get_height() * self.prop))
                )
                self.rect = self.image.get_rect(center=self.rect.center)
                new_font_size = int(self.base_font_size * self.prop)
                self.update_text_surface(new_font_size)
                self.hovered = True
        else:
            if self.hovered:
                self.image = self.original_image
                self.rect = self.image.get_rect(center=self.rect.center)
                self.update_text_surface(self.base_font_size)
                self.hovered = False

        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def initialiser(self, screen):
        screen.blit(self.image, self.rect.topleft)
        screen.blit(self.text_surface, self.text_rect.topleft)

    def clique(self, event, mouse_pos):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(mouse_pos)