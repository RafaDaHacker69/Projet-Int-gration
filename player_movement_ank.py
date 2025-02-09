import pygame

class Player:
    def __init__(self, x_position, y_position, width, height, controls):
        # Initial player setup
        self.x_position = x_position
        self.y_position = y_position
        self.width = width
        self.height = height
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = True
        self.max_speed = 6
        self.gravity = 0.3
        self.jump_force = 7
        self.acceleration = 0.5  # Acceleration when moving
        self.friction = 0.1  # Deceleration when no keys are pressed
        self.controls = controls  # Controls (e.g., 'wasd' or 'arrows')

    def handle_input(self, keys):
        move_direction = 0

        if self.controls == 'wasd':
            if keys[pygame.K_a]:
                move_direction = -1
            elif keys[pygame.K_d]:
                move_direction = 1
            if keys[pygame.K_w] and self.on_ground:
                self.on_ground = False
                self.velocity_y = -self.jump_force
        elif self.controls == 'arrows':
            if keys[pygame.K_LEFT]:
                move_direction = -1
            elif keys[pygame.K_RIGHT]:
                move_direction = 1
            if keys[pygame.K_UP] and self.on_ground:
                self.on_ground = False
                self.velocity_y = -self.jump_force

        # Apply acceleration
        self.velocity_x += move_direction * self.acceleration

        # Limit max speed
        self.velocity_x = max(-self.max_speed, min(self.velocity_x, self.max_speed))

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity_y += self.gravity
            self.y_position += self.velocity_y

    def apply_friction(self):
        if self.velocity_x > 0:
            self.velocity_x = max(0, self.velocity_x - self.friction)
        elif self.velocity_x < 0:
            self.velocity_x = min(0, self.velocity_x + self.friction)

    def check_collisions(self, base_y_position):
        # Ground collision check
        if self.y_position >= base_y_position:
            self.y_position = base_y_position
            self.velocity_y = 0
            self.on_ground = True

    def update_position(self):
        self.x_position += self.velocity_x
        self.apply_friction()  # Apply friction after updating position

    def draw(self, game_display, color):
        pygame.draw.rect(game_display, color, (self.x_position, self.y_position, self.width, self.height))
