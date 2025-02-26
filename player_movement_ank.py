import pygame

class Player:
    def __init__(self, x_position, y_position, width, height, controls):
        self.rect = pygame.Rect(x_position, y_position, width, height)
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.gravity = 0.3
        self.jump_force = 7
        self.acceleration = 0.5
        self.friction = 0.1
        self.controls = controls


    def handle_input(self, keys):
        move_direction = 0
        if self.controls == 'wasd':
            if keys[pygame.K_a]:
                move_direction = -1
            elif keys[pygame.K_d]:
                move_direction = 1
            if keys[pygame.K_w] and self.on_ground:
                self.velocity_y = -self.jump_force
                self.on_ground = False
        elif self.controls == 'arrows':
            if keys[pygame.K_LEFT]:
                move_direction = -1
            elif keys[pygame.K_RIGHT]:
                move_direction = 1
            if keys[pygame.K_UP] and self.on_ground:
                self.velocity_y = -self.jump_force
                self.on_ground = False

        self.velocity_x += move_direction * self.acceleration
        self.velocity_x = max(-6, min(self.velocity_x, 6))

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity_y += self.gravity

    def check_collisions(self, obstacles):
        self.on_ground = False  # Reset ground check

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                # Check if landing on top of an obstacle
                if self.velocity_y > 0 and self.rect.bottom > obstacle.rect.top:
                    self.rect.bottom = obstacle.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                # Check for wall collisions (left/right)
                elif self.velocity_x > 0 and self.rect.right > obstacle.rect.left:
                    self.rect.right = obstacle.rect.left
                    self.velocity_x = 0
                elif self.velocity_x < 0 and self.rect.left < obstacle.rect.right:
                    self.rect.left = obstacle.rect.right
                    self.velocity_x = 0

    def update_position(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def draw(self, game_display, color):
        pygame.draw.rect(game_display, color, self.rect)