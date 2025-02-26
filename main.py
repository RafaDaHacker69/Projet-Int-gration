
import pygame.event
from player_movement_ank import Player
from Bras_Rotatif import Bras_Rotatif
from Boules_De_Neiges import Boules_De_Neiges
from Obstacle_collision import Obstacle

pygame.init()

game_display = pygame.display.set_mode((1240, 680))
game_clock = pygame.time.Clock()

BACKGROUND_COLOR = pygame.Color('white')
display_width, display_height = game_display.get_size()

player1 = Player(display_width * 0.2, display_height * 0.8, 30, 40, controls='wasd')
player2 = Player(display_width * 0.7, display_height * 0.8, 30, 40, controls='arrows')

player_image1 = pygame.image.load("IMAGES/Cat.jpg").convert_alpha()
Image_Witdh=player_image1.get_width()
Image_Height = player_image1.get_height()
player1_image_flip = None

player_image2 = pygame.image.load("IMAGES/Dog.jpg").convert_alpha()
Image_Witdh2=player_image2.get_width()
Image_Height2 = player_image2.get_height()
player2_image_flip = None

player1_image_flip = pygame.transform.flip(player_image1, True, False)
player2_image_flip = pygame.transform.flip(player_image2, False, False)

bras_rotatif = Bras_Rotatif(0,0.001,0,0,0.03,False,False,0)
bras_rotatif2 = Bras_Rotatif(0,0.001,0,0,0.03,False,False,0)

rect = pygame.Surface((100,80),pygame.SRCALPHA)
rect2 = pygame.Surface((100,80),pygame.SRCALPHA)
#rect.fill("green")
#rect2.fill("yellow")

#Bras des personnages
pygame.draw.rect(rect,(255,0,0),(45,30,40,20))
pygame.draw.rect(rect2,(0, 120, 250),(15,30,40,20))

#Mains des personnages
pygame.draw.rect(rect,(0,0,0),(85,30,10,20))
pygame.draw.rect(rect2,(0,0,0),(5,30,10,20))

#variables bras
posx = player1.x_position
posy = player1.y_position
posx2 = player2.x_position
posy2 = player2.y_position

game_display.blit(rect,(posx,posy))

player_y_Baseposition = display_height * 0.8

i=0
i2=0
t=0
t2=0
omega=0
omega2=0
rec_taille=rect.get_rect()
rec_centre_x=rec_taille.center[0]
rec_centre_y=rec_taille.center[1]
rec_taille2=rect2.get_rect()
rec_centre_x2=rec_taille2.center[0]
rec_centre_y2=rec_taille2.center[1]

#creation obstacles
Obstacle_collision = [
    Obstacle(200, 450, 100, 20),  # Floating platform
    Obstacle(400, 350, 150, 20),  # Another platform
    Obstacle(600, 500, 50, 100)  # Wall
]
#End variables

game_running = True
while game_running:

    keys = pygame.key.get_pressed()

    # Gérer l'entrée utilisateur
    player1.handle_input(keys)
    player2.handle_input(keys)

    # Appliquer la friction
    player1.apply_friction()
    player2.apply_friction()

    # Appliquer la gravité
    player1.apply_gravity()
    player2.apply_gravity()

    # Mettre à jour les positions
    player1.update_position()
    player2.update_position()

    # Vérifier les collisions avec le sol
    player1.check_collisions(player_y_Baseposition)
    player2.check_collisions(player_y_Baseposition)

    # Limites de l'écran pour le déplacement des joueurs
    if player1.x_position < 0:
        player1.x_position = 0
        posx = player1.x_position
    elif player1.x_position + player1.width > display_width / 2:  # Prevents clipping
        player1.x_position = display_width / 2 - player1.width
        posx = player1.x_position

    if player2.x_position > display_width - 20:
        player2.x_position = display_width - 20
        posx2 = player2.x_position
    elif player2.x_position < display_width / 2:
        player2.x_position = display_width / 2
        posx2 = player2.x_position

#flip image functions
    direction1 = player1.get_movement_direction()
    direction2 = player2.get_movement_direction()

    if direction1 == "right":
        player1_image_flip = pygame.transform.flip(player_image1,True,False)
    elif direction1 == "left":
        player1_image_flip = pygame.transform.flip(player_image1, False, False)

    if direction2 == "right":
        player2_image_flip = pygame.transform.flip(player_image2,True,False)
    elif direction2 == "left":
        player2_image_flip = pygame.transform.flip(player_image2, False, False)

    # Rendu graphique
    game_display.fill(BACKGROUND_COLOR)

    #player1.draw(game_display, (0, 120, 250))
    player_rect1 = player_image1.get_rect(center=(player1.x_position+140, player1.y_position+120))
    imageFinal1 = pygame.transform.scale_by(player1_image_flip, 0.3)
    game_display.blit(imageFinal1, player_rect1)

    #player2.draw(game_display, (255, 0, 0))
    player_rect2 = player_image2.get_rect(center=(player2.x_position + 300, player2.y_position + 400))
    imageFinal2 = pygame.transform.scale_by(player2_image_flip, 0.12)
    game_display.blit(imageFinal2, player_rect2)

    pygame.draw.rect(game_display, (0, 0, 0), (0, player_y_Baseposition + 40, display_width, 5))
    pygame.draw.rect(game_display, (255, 0, 0), (display_width / 2, 0, 1, display_height))

# Physique rotation bras
    if keys[pygame.K_LSHIFT]:
        t += 0.01
        i -= bras_rotatif.calcul_de_vitesse_angulaire(t,omega)
        print(f"Accélération angulaire {bras_rotatif.alpha}:")
        print(f"Vitesse angulaire {bras_rotatif.v}:")
        print(f"Angle théta {bras_rotatif.theta}:")
        print(f"Temps {t}:")
        print(f"I {i}:")
        if i<-360:
            i=0

    if keys[pygame.K_m]:
        t2 += 0.01
        i2 += bras_rotatif2.calcul_de_vitesse_angulaire(t2,omega2)
        if i2>360:
            i2=0
#Ramasser une boule de neige
    if bras_rotatif.ferme and bras_rotatif.boule == False and -65 > i > -115:
        boule = Boules_De_Neiges(0.01, 0.01)

        bras_rotatif.boule = True
        print(f"Boule de neige {bras_rotatif.boule}:")

    if bras_rotatif2.ferme and bras_rotatif2.boule == False and 115 > i2 > 65:
        boule = Boules_De_Neiges(0.01, 0.01)
        #pygame.draw.circle(0,(255,255,255),0,boule.r)
        bras_rotatif2.boule = True
        print(f"Boule de neige {bras_rotatif2.boule}:")


#Fermeture de la main
    if keys[pygame.K_c]:
        pygame.draw.rect(rect, (0, 255, 0), (85, 30, 10, 20))
        bras_rotatif.ferme=True
    if keys[pygame.K_n]:
        pygame.draw.rect(rect2, (0, 255, 0), (5, 30, 10, 20))
        bras_rotatif2.ferme = True


# Rotation bras
    rect_rotated = pygame.transform.rotate(rect, i)
    rectangle_rot_taille = rect_rotated.get_rect()
    rectangle_rot_centre_x = rectangle_rot_taille.center[0]
    rectangle_rot_centre_y = rectangle_rot_taille.center[1]
    diff_x = rectangle_rot_centre_x - rec_centre_x
    diff_y = rectangle_rot_centre_y - rec_centre_y

    rect_rotated2 = pygame.transform.rotate(rect2, i2)
    rectangle_rot_taille2 = rect_rotated2.get_rect()
    rectangle_rot_centre_x2 = rectangle_rot_taille2.center[0]
    rectangle_rot_centre_y2 = rectangle_rot_taille2.center[1]
    diff_x2 = rectangle_rot_centre_x2 - rec_centre_x2
    diff_y2 = rectangle_rot_centre_y2 - rec_centre_y2

    game_display.blit(rect_rotated, (player1.x_position - diff_x -30, player1.y_position - diff_y-30))
    game_display.blit(rect_rotated2, (player2.x_position - diff_x2-40, player2.y_position - diff_y2-30))

# Key binding
    for game_event in pygame.event.get():
        if game_event.type == pygame.QUIT:
            game_running = False
        if game_event.type == pygame.KEYUP:
            if game_event.key == pygame.K_LSHIFT:
                t = 0
                bras_rotatif.omega = 0.03
                omega=0
                print(f" Shift Up {t}:")
            if game_event.key == pygame.K_m:
                t2 = 0
                bras_rotatif2.omega = 0.03
                omega2=0
            if game_event.key == pygame.K_c:
                pygame.draw.rect(rect, (0, 0, 0), (85, 30, 10, 20))
                bras_rotatif.ferme = False
                bras_rotatif.boule = False
                #print(f"Boule de neige {bras_rotatif.boule}:")
            if game_event.key == pygame.K_n:
                pygame.draw.rect(rect2,(0,0,0),(5,30,10,20))
                bras_rotatif2.ferme = False
                bras_rotatif2.boule = False
                print(f"Boule de neige {bras_rotatif.boule}:")

    #print(f"Angle du bras {i2}:")
    pygame.display.update()

    game_clock.tick(60)

pygame.quit()
