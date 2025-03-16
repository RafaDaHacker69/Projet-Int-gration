import pygame


class Player:
    def __init__(self, x_position, y_position, width, height, controls):
        self.x_position = x_position
        self.y_position = y_position
        self.width = width
        self.height = height
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.max_speed = 6
        self.gravity = 0.2
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
        self.velocity_x = max(-self.max_speed, min(self.velocity_x, self.max_speed))

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity_y += self.gravity

    def apply_friction(self):
        if self.velocity_x > 0:
            self.velocity_x = max(0, self.velocity_x - self.friction)
        elif self.velocity_x < 0:
            self.velocity_x = min(0, self.velocity_x + self.friction)

    def check_ground_collision(self, ground_level):
        """Checks if the player is on the ground."""
        if self.y_position + self.height >= ground_level:
            self.y_position = ground_level - self.height  # Align player with the ground
            self.velocity_y = 0  # Stop downward movement
            self.on_ground = True
        else:
            self.on_ground = False

    def check_obstacle_collisions(self, obstacles):
        """Handles player collision with obstacles on all sides."""

        # Future position for collision checking
        next_x = self.x_position + self.velocity_x
        next_y = self.y_position + self.velocity_y

        # Create Rects for movement prediction
        player_rect_x = pygame.Rect(next_x, self.y_position, self.width, self.height)
        player_rect_y = pygame.Rect(self.x_position, next_y, self.width, self.height)

        # Check horizontal movement collision
        for obstacle in obstacles:
            if player_rect_x.colliderect(obstacle.rect):
                if self.velocity_x > 0:  # Moving right
                    self.x_position = obstacle.rect.left - self.width
                elif self.velocity_x < 0:  # Moving left
                    self.x_position = obstacle.rect.right
                self.velocity_x = 0  # Stop horizontal movement
                break  # Stop checking other obstacles

        # Check vertical movement collision
        for obstacle in obstacles:
            if player_rect_y.colliderect(obstacle.rect):
                if self.velocity_y > 0:  # Falling down
                    self.y_position = obstacle.rect.top - self.height
                    self.on_ground = True
                elif self.velocity_y < 0:  # Jumping up
                    self.y_position = obstacle.rect.bottom
                self.velocity_y = 0  # Stop vertical movement
                break  # Stop checking other obstacles

    def update_position(self, obstacles):
        self.apply_gravity()
        self.check_obstacle_collisions(obstacles)
        self.apply_friction()

        # Apply final movement
        self.x_position += self.velocity_x
        self.y_position += self.velocity_y

    def get_movement_direction(self):
        if self.velocity_x > 0:
            return 1  # Moving right
        elif self.velocity_x < 0:
            return -1  # Moving left
        return 0  # Standing still

    def draw(self, game_display, color):
        pygame.draw.rect(game_display, color, (self.x_position, self.y_position, self.width, self.height))