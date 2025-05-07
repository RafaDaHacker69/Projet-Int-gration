

from Bras_Rotatif import *

class Player:
    def __init__(self, position_x, position_y, largeur, hauteur, controles, pv, inverse):
        self.position_x = position_x
        self.previous_position_x = 0
        self.position_y = position_y
        self.largeur = largeur
        self.hauteur = hauteur
        self.Stamina = 100
        self.max_Stamina = 100
        self.dernier_Stamina_util = pygame.time.get_ticks()
        self.vitesse_x = 0
        self.vitesse_y = 0
        self.au_sol = False
        self.sur_plateforme = False
        self.dernier_obstacle = None
        self.vitesse_max = 6
        self.vitesse_max_base = 6
        self.gravite = 0.2
        self.force_saut = 7
        self.acceleration = 0.6
        self.snow_acceleration = 0.6
        self.ice_acceleration= 0.2
        self.friction = 0.3
        self.snow_friction = 0.2
        self.ice_friction = 0.05
        self.controles = controles
        self.hitboxe = None
        self.pv = pv
        self.pv_max = 100
        self.charge=0
        self.charge_max = 100
        self.facteur= 0.01
        self.image = pygame.image.load("IMAGES/finalmodel.png").convert_alpha()
        self.joueurSorte=1
        self.bras_obj = None
        self.mur = False
        self.position_x_mur = 0
        self.position_y_mur = 0
        self.ulti_dmg = 0
        self.ult_dmg = False
        self.compteur = 0
        #Sprite animation
        self.animation_frames = []
        self.frame_index = 0
        self.animation_speed = 0.2
        self.frame_timer = 0
        self.last_direction = -1
        self.inverse = inverse
        #idle sprite animation
        self.Idle_animation_frames = []
        self.Idle_frame_index = 0
        self.Idle_animation_speed = 0.2
        self.Idle_frame_timer = 0
        self.Idle_last_direction = -1
        self.Idle_inverse = inverse
        self.nbJoueur=1

    def load_sprite_sheet(self, path, num_frames):
        sprite_sheet = pygame.image.load(path).convert_alpha()
        frame_width = sprite_sheet.get_width() // num_frames
        frame_height = sprite_sheet.get_height()
        for i in range(num_frames):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            self.animation_frames.append(frame)

    def load_idle_sprite_sheet(self, path, num_frames):
        sprite_sheet = pygame.image.load(path).convert_alpha()
        frame_width = sprite_sheet.get_width() // num_frames
        frame_height = sprite_sheet.get_height()
        for i in range(num_frames):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            self.Idle_animation_frames.append(frame)

    def update_idle_animation(self):
        self.Idle_frame_timer += self.Idle_animation_speed
        if self.Idle_frame_timer >= 1:
            self.Idle_frame_index = (self.Idle_frame_index + 1) % len(self.Idle_animation_frames)
            self.Idle_frame_timer = 0

    def update_animation(self):
        if self.position_x != self.previous_position_x:
            speed_ratio = abs(self.vitesse_x) / self.vitesse_max_base
            speed_ratio = min(speed_ratio, 1)

            self.frame_timer += speed_ratio

            if self.frame_timer >= 1:
                self.frame_index += 1
                self.frame_timer = 0

                if self.frame_index >= len(self.animation_frames):
                    self.frame_index = 0
            self.update_idle_animation()
        else:
            self.update_idle_animation()
            self.frame_index = 0
            self.frame_timer = 0

        self.previous_position_x = self.position_x

    def get_current_frame(self):
        if self.vitesse_x != 0:
            return self.animation_frames[self.frame_index]
        else:
            return self.Idle_animation_frames[self.Idle_frame_index]

    def util_stamina(self, nb):
        if self.Stamina >= nb:
            self.Stamina -= nb
            self.dernier_Stamina_util = pygame.time.get_ticks()

    def handle_input(self, keys):
        direction_mouvement = 0
        if self.Stamina >= 5:
            if self.controles == 'wasd':
                if keys[pygame.K_a]:
                    direction_mouvement = -1
                    self.util_stamina(0.1)
                    self.last_direction = -1
                elif keys[pygame.K_d]:
                    direction_mouvement = 1
                    self.util_stamina(0.1)
                    self.last_direction = 1
                if keys[pygame.K_w] and self.au_sol:
                    self.vitesse_y = -self.force_saut
                    self.au_sol = False
                    self.sur_plateforme = False
                    self.util_stamina(5)
            elif self.controles == 'fleches':
                if keys[pygame.K_LEFT]:
                    direction_mouvement = -1
                    self.util_stamina(0.1)
                    self.last_direction = -1
                elif keys[pygame.K_RIGHT]:
                    direction_mouvement = 1
                    self.util_stamina(0.1)
                    self.last_direction = 1
                if keys[pygame.K_UP] and self.au_sol:
                    self.vitesse_y = -self.force_saut
                    self.au_sol = False
                    self.sur_plateforme = False
                    self.util_stamina(5)

        self.vitesse_x += direction_mouvement * self.acceleration
        self.vitesse_x = max(-self.vitesse_max, min(self.vitesse_x, self.vitesse_max))

    def heal_Stamina(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.dernier_Stamina_util >= 2000:
            if self.Stamina < self.max_Stamina:
                if (current_time - self.dernier_Stamina_util) % 500 < 50:
                    self.Stamina = min(self.max_Stamina, self.Stamina + 5)
    def charger(self):
        if self.charge < self.charge_max:
            self.charge += self.facteur
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
            self.friction = self.ice_friction
            self.acceleration = self.ice_acceleration
            #print("friction:" + str(self.friction))
        else:
            if self.sur_plateforme == True:
                self.au_sol = True
            else:
                self.au_sol = False
                self.friction = self.snow_friction
                self.acceleration = self.snow_acceleration
                #print("friction:" + str(self.friction))

    def ult(self):
        if self.charge>=self.charge_max:
            print("ult: ")
            print(self.joueurSorte)
            self.charge=0
            if self.joueurSorte == 1:
                self.pv += 25
                if (self.pv>self.pv_max):
                    self.pv = self.pv_max
                print(self.pv)
            if self.joueurSorte == 2:
                self.ulti_dmg = 20
                self.ult_dmg = True
                print("utl 2")
            if self.joueurSorte == 3:
                self.mur = True
                self.position_x_mur = self.position_x + 80
                self.position_y_mur = self.position_y - 70
                if self.inverse:
                    self.position_x_mur = self.position_x - 90
                    self.position_y_mur = self.position_y - 70
                print("utl 3")


    def check_obstacle_collisions(self, obstacles):
        prochain_x = self.position_x + self.vitesse_x
        prochain_y = self.position_y + self.vitesse_y

        rect_joueur_x = pygame.Rect(prochain_x, self.position_y, self.largeur, self.hauteur)
        rect_joueur_y = pygame.Rect(self.position_x, prochain_y, self.largeur, self.hauteur)

        self.au_sol = False

        if self.dernier_obstacle:
            if self.vitesse_x > 0:
                if prochain_x >= (self.dernier_obstacle.rect.left - self.largeur + (self.dernier_obstacle.get_width())):
                    if self.sur_plateforme:
                        self.vitesse_y += self.gravite
                        self.sur_plateforme = False
            elif  self.vitesse_x < 0:
                if prochain_x < (self.dernier_obstacle.rect.right-(self.dernier_obstacle.get_width()+self.largeur)):
                    if self.sur_plateforme:
                        self.vitesse_y += self.gravite
                        self.sur_plateforme = False

        MAX_STEP_HEIGHT = 40
        for obstacle in obstacles:
            if rect_joueur_x.colliderect(obstacle.rect):
                obstacle_top = obstacle.rect.top
                obstacle_bottom = obstacle.rect.bottom
                player_bottom = self.position_y + self.hauteur

                height_diff = obstacle_top - player_bottom

                if 0 < -height_diff <= MAX_STEP_HEIGHT:
                    self.position_y += height_diff*0.8
                    self.position_x = obstacle.rect.left - self.largeur if self.vitesse_x > 0 else obstacle.rect.right
                    self.vitesse_y = 0
                    self.au_sol = True
                    self.sur_plateforme = True
                    self.dernier_obstacle = obstacle
                else:
                    if self.vitesse_x > 0:
                        self.position_x = obstacle.rect.left - self.largeur
                    else:
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
                    self.dernier_obstacle = obstacle
                elif self.vitesse_y < 0:
                    self.position_y = obstacle.rect.bottom
                    self.vitesse_y = 0
                break

    def vitesse_selon_Stamina(self):
        pourcentage = self.Stamina/self.max_Stamina
        if pourcentage > 0.70:
            self.vitesse_max = self.vitesse_max_base * pourcentage
        else:
            pourcentage = 0.70
            self.vitesse_max = self.vitesse_max_base * pourcentage


    def update_position(self, obstacles):
        self.apply_gravity()
        self.check_obstacle_collisions(obstacles)
        self.apply_friction()

        self.position_x += self.vitesse_x
        self.position_y += self.vitesse_y

        self.heal_Stamina()
        self.charger()
        self.vitesse_selon_Stamina()
        #print(f"Stamina: {self.Stamina}/{self.max_Stamina}")

    def get_movement_direction(self):
        if self.vitesse_x > 0:
            return 1
        elif self.vitesse_x < 0:
            return -1
        return 0

    def reset_ulti_dmg(self):
        if self.ult_dmg:
            self.compteur+=1
            #print(self.compteur)
            if self.compteur == 900:
                self.ulti_dmg = 0
                self.ult_dmg = False
                self.compteur = 0
                print("ult terminé")

    def draw(self, game_display, color):
        #pygame.draw.rect(game_display, color, (self.position_x, self.position_y, self.largeur, self.hauteur))
        current_frame = self.get_current_frame()
        flipped = pygame.transform.flip(current_frame, self.last_direction == -1, False)
        game_display.blit(flipped, (self.position_x, self.position_y))

    def hitboxes(self,screen):
        if self.inverse :
            hitbox_width = 70
            hitbox_height = 95
            player_hitboxe = pygame.Rect(self.position_x - 17,#23
                                         self.position_y - hitbox_height // 2,
                                         hitbox_width, hitbox_height)
            self.hitboxe = player_hitboxe
        else :
            hitbox_width = 70
            hitbox_height = 95
            player_hitboxe = pygame.Rect(self.position_x - 17,#23
                                         self.position_y - hitbox_height // 2,
                                         hitbox_width, hitbox_height)
            self.hitboxe = player_hitboxe
        #Dessin de la hitboxe du joueur
        #pygame.draw.rect(screen, (0, 255, 0, 128), player_hitboxe, 2)  # Transparent Green Border