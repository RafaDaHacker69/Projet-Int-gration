import pygame

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.contact = 0
        self.original_y = y
        self.original_height = height
        self.taille_x = width
        self.taille_y = height
        self.growth_speed = 0.6
        self.last_growth_time = pygame.time.get_ticks()
        self.growth_delay = 2000

    def draw(self, game_display, color):
        pygame.draw.rect(game_display, color, self.rect)

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def get_y_pos(self):
        return self.rect.y

    def is_player_on_top(self, player):
        player_rect = player.hitboxe
        obstacle_top = self.rect.top
        return player_rect.bottom >= obstacle_top and player_rect.bottom <= obstacle_top + 20 and player_rect.colliderect(
            self.rect)

    def regrow(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_growth_time >= self.growth_delay:
            self.last_growth_time = current_time

            if self.rect.height < self.original_height:
                growth_per_frame = self.growth_speed
                self.rect.height += growth_per_frame
                self.rect.y -= growth_per_frame

                if self.rect.height > self.original_height:
                    self.rect.height = self.original_height
                    self.rect.y = self.original_y - self.rect.height
