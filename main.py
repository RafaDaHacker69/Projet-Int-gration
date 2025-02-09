import pygame
import pygame.event
from player_movement_ank import Player
from Bras_Rotatif import Bras_Rotatif

pygame.init()

game_display = pygame.display.set_mode((1240, 680))
game_clock = pygame.time.Clock()

BACKGROUND_COLOR = pygame.Color('white')
display_width, display_height = game_display.get_size()

player1 = Player(display_width * 0.2, display_height * 0.8, 30, 40, controls='wasd')
player2 = Player(display_width * 0.7, display_height * 0.8, 30, 40, controls='arrows')

bras_rotatif = Bras_Rotatif(0,0.01,0,0)
bras_rotatif2 = Bras_Rotatif(0,0.01,0,0)

rect = pygame.Surface((100,80),pygame.SRCALPHA)
rect2 = pygame.Surface((100,80),pygame.SRCALPHA)
#rect.fill("green")
#rect2.fill("yellow")

pygame.draw.rect(rect,(255,0,0),(45,30,40,20))
pygame.draw.rect(rect2,(0, 120, 250),(15,30,40,20))

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

    # Rendu graphique
    game_display.fill(BACKGROUND_COLOR)

    player1.draw(game_display, (0, 120, 250))
    player2.draw(game_display, (255, 0, 0))

    pygame.draw.rect(game_display, (0, 0, 0), (0, player_y_Baseposition + 40, display_width, 5))
    pygame.draw.rect(game_display, (255, 0, 0), (display_width / 2, 0, 1, display_height))


    if keys[pygame.K_LSHIFT]:
        t += 0.1
        i -= bras_rotatif.Calcul_de_vitesse_angulaire(omega, t, bras_rotatif.alpha, bras_rotatif.theta)
    if keys[pygame.K_m]:
        t2 += 0.1
        i2 += bras_rotatif.Calcul_de_vitesse_angulaire(omega2, t2, bras_rotatif2.alpha, bras_rotatif2.theta)

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

    #game_display.blit(rect_rotated, (posx - diff_x, posy - diff_y))
    #game_display.blit(rect_rotated2, (posx2 - diff_x2, posy2 - diff_y2))
    game_display.blit(rect_rotated, (player1.x_position - diff_x -30, player1.y_position - diff_y-30))
    game_display.blit(rect_rotated2, (player2.x_position - diff_x2-40, player2.y_position - diff_y2-30))


    for game_event in pygame.event.get():
        if game_event.type == pygame.QUIT:
            game_running = False
        if game_event.type == pygame.KEYUP:
            if game_event.key == pygame.K_LSHIFT:
                t = 0
            if game_event.key == pygame.K_m:
                t2 = 0

    pygame.display.update()

    game_clock.tick(60)

pygame.quit()
