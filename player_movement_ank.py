import pygame


class Player:
    def __init__(self, position_x, position_y, largeur, hauteur, controles, Stamina):
        self.position_x = position_x
        self.position_y = position_y
        self.largeur = largeur
        self.hauteur = hauteur
        self.vitesse_x = 0
        self.vitesse_y = 0
        self.au_sol = False
        self.sur_plateforme = False
        self.vitesse_max = 6
        self.gravite = 0.2
        self.force_saut = 7
        self.acceleration = 0.5
        self.friction = 0.1
        self.controles = controles
        self.hitboxe = None
        self.pv = 100
        self.Stamina = Stamina

    def handle_input(self, keys):
        direction_mouvement = 0
        if self.controles == 'wasd':
            if keys[pygame.K_a]:
                direction_mouvement = -1
                self.Stamina -= 5
            elif keys[pygame.K_d]:
                direction_mouvement = 1
                self.Stamina -= 5
            if keys[pygame.K_w] and self.au_sol:
                self.vitesse_y = -self.force_saut
                self.au_sol = False
                self.sur_plateforme = False
                self.Stamina -= 25
        elif self.controles == 'fleches':
            if keys[pygame.K_LEFT]:
                direction_mouvement = -1
            elif keys[pygame.K_RIGHT]:
                direction_mouvement = 1
            if keys[pygame.K_UP] and self.au_sol:
                self.vitesse_y = -self.force_saut
                self.au_sol = False
                self.sur_plateforme = False

        self.vitesse_x += direction_mouvement * self.acceleration
        self.vitesse_x = max(-self.vitesse_max, min(self.vitesse_x, self.vitesse_max))

    def apply_gravity(self):
        if not self.au_sol:
            self.vitesse_y += self.gravite

    def apply_friction(self):
        if self.vitesse_x > 0:
            self.vitesse_x = max(0, self.vitesse_x - self.friction)
        elif self.vitesse_x < 0:
            self.vitesse_x = min(0, self.vitesse_x + self.friction)

    def check_ground_collision(self, ground_level):
        if self.position_y + self.hauteur >= ground_level:
            self.position_y = ground_level - self.hauteur
            self.vitesse_y = 0
            self.au_sol = True
        else:
            if self.sur_plateforme == True:
                self.au_sol = True
            else:
                self.au_sol = False

    def check_obstacle_collisions(self, obstacles):
        prochain_x = self.position_x + self.vitesse_x
        prochain_y = self.position_y + self.vitesse_y

        rect_joueur_x = pygame.Rect(prochain_x, self.position_y, self.largeur, self.hauteur)
        rect_joueur_y = pygame.Rect(self.position_x, prochain_y, self.largeur, self.hauteur)

        self.au_sol = False

        for obstacle in obstacles:
            if rect_joueur_x.colliderect(obstacle.rect):
                if self.vitesse_x > 0:
                    self.position_x = obstacle.rect.left - self.largeur
                elif self.vitesse_x < 0:
                    self.position_x = obstacle.rect.right
                self.vitesse_x = 0
                break

        for obstacle in obstacles:
            if rect_joueur_y.colliderect(obstacle.rect):
                if self.vitesse_y > 0:
                    self.position_y = obstacle.rect.top - self.hauteur
                    self.vitesse_y = 0
                    self.au_sol = True
                    self.sur_plateforme = True
                elif self.vitesse_y < 0:
                    self.position_y = obstacle.rect.bottom
                    self.vitesse_y = 0
                break

    def update_position(self, obstacles):
        self.apply_gravity()
        self.check_obstacle_collisions(obstacles)
        self.apply_friction()

        self.position_x += self.vitesse_x
        self.position_y += self.vitesse_y

    def get_movement_direction(self):
        if self.vitesse_x > 0:
            return 1
        elif self.vitesse_x < 0:
            return -1
        return 0

    def draw(self, game_display, color):
        pygame.draw.rect(game_display, color, (self.position_x, self.position_y, self.largeur, self.hauteur))

    def hitboxes(self,screen):
        hitbox_width = 70
        hitbox_height = 85
        player_hitboxe = pygame.Rect(self.position_x - hitbox_width // 3,
                                     self.position_y - hitbox_height // 2,
                                     hitbox_width, hitbox_height)
        self.hitboxe = player_hitboxe
        #Dessin de la hitboxe du joueur
        #pygame.draw.rect(screen, (0, 255, 0, 128), player_hitboxe, 2)  # Transparent Green Border