import pygame.event
from menu import *
from Bar import *
from Test_menu import Menu
from player import Player
from Bras_Rotatif import Bras_Rotatif
from Obstacle_collision import Obstacle

pygame.init()

game_display = pygame.display.set_mode((1240, 680))
menu_display = pygame.display.set_mode((1,1))
pygame.display.set_caption('CP (Club Penguin)')

menu_principale = menu(menu_display)
menu_principale.menu()

game_clock = pygame.time.Clock()

BACKGROUND_COLOR = pygame.Color('white')
bg = pygame.image.load('IMAGES/Bg.jpg').convert_alpha()
sol = pygame.image.load('IMAGES/sol.png').convert_alpha()
display_width, display_height = game_display.get_size()

player1 = Player(display_width * 0.2, display_height * 0.8, 30, 40, controles='wasd')
player2 = Player(display_width * 0.7, display_height * 0.8, 30, 40, controles='fleches')

bras_rotatif = Bras_Rotatif(1,0,4,False)
bras_rotatif2 = Bras_Rotatif(1,0,4,True)

#Menu de séléction des perso
menu_perso1 = menu(menu_display)
menu_perso1.selection_perso(player1, bras_rotatif,"Sélection du Joueur 1")

menu_perso2 = menu(menu_display)
menu_perso2.selection_perso(player2, bras_rotatif2,"Sélection du Joueur 2")

#Menu de mort du joueur
menu_de_mort1 = menu(menu_display)
menu_de_mort2 = menu(menu_display)

player_image1 = player1.image
Image_Witdh=player_image1.get_width()
Image_Height = player_image1.get_height()
player1_image_flip = None

player_image2 = player2.image
Image_Witdh2=player_image2.get_width()
Image_Height2 = player_image2.get_height()
player2_image_flip = None

player1_image_flip = pygame.transform.flip(player_image1, True, False)
player2_image_flip = pygame.transform.flip(player_image2, False, False)

bras_rect = bras_rotatif.creation_bras_main(255,0,0)
bras_rect2 = bras_rotatif2.creation_bras_main(0,120,250)

player_y_Baseposition = display_height*0.88

#creation obstacles
Obstacle_collision = [
    Obstacle(100, display_height-90, 50, 50),  # Floating platform
    Obstacle(120, display_height-100, 50, 50),  # Another platform
    Obstacle(140, display_height-110, 50, 50),  # Wall
    Obstacle(160, display_height - 100, 50, 50),  # Another platform
    Obstacle(180, display_height - 90, 50, 50),  # Floating platform

    Obstacle(320, display_height - 200, 50, 100),  # Floating platform
]
#End variables
while menu_principale.run:
    if menu_de_mort1.restart or menu_de_mort2.restart:
        menu_perso1.selection_perso(player1, bras_rotatif, "Sélection du Joueur 1")
        menu_perso2.selection_perso(player2, bras_rotatif2, "Sélection du Joueur 2")
        player_image1 = player1.image
        player_image2 = player2.image
        player1.position_x = display_width * 0.2
        player1.position_y = display_height * 0.8
        player2.position_x = display_width * 0.7
        player2.position_y = display_height * 0.8
        player1.vitesse_x = 0
        player1.vitesse_y = 0
        player2.vitesse_x = 0
        player2.vitesse_y = 0
        player1.pv = 100
        player1.stamina = 200
        player2.pv = 100
        player2.stamina = 200
        bras_rotatif.theta = 0
        bras_rotatif2.theta = 0
        bras_rotatif.omega = 0
        bras_rotatif2.omega = 0
        menu_de_mort1.restart = False
        menu_de_mort2.restart = False

    keys = pygame.key.get_pressed()

    for player in (player1, player2):
        player.handle_input(keys)
        player.apply_friction()
        player.apply_gravity()
        player.update_position(Obstacle_collision)
        player.check_ground_collision(player_y_Baseposition)
    # Limites de l'écran pour le déplacement des joueurs
    if player1.position_x < 0:
        player1.position_x = 0
        posx = player1.position_x
    elif player1.position_x + player1.largeur > display_width / 2:  # Prevents clipping
        player1.position_x = display_width / 2 - player1.largeur
        posx = player1.position_x

    if player2.position_x > display_width - 20:
        player2.position_x = display_width - 20
        posx2 = player2.position_x
    elif player2.position_x < display_width / 2:
        player2.position_x = display_width / 2
        posx2 = player2.position_x

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

#Rendu graphique
    game_display.fill(BACKGROUND_COLOR)
    game_display.blit(bg, (0, 0))
    game_display.blit(sol,(0,585))

    player1.hitboxes(game_display)
    player2.hitboxes(game_display)

    #player1.draw(game_display, (0, 120, 250))
    #player_rect1 = player_image1.get_rect(center=(player1.x_position+Decalage_x_p1, player1.y_position+Decalage_y_p1))
    imageFinal1 = pygame.transform.scale_by(player1_image_flip, 0.4)
    image_rect1 = imageFinal1.get_rect(center=player1.hitboxe.center)

    #player2.draw(game_display, (255, 0, 0))
    #player_rect2 = player_image2.get_rect(center=(player2.x_position + Decalage_x_p2, player2.y_position + Decalage_y_p2))
    imageFinal2 = pygame.transform.scale_by(player2_image_flip, 0.4)
    image_rect2 = imageFinal2.get_rect(center=player2.hitboxe.center)

    game_display.blit(imageFinal1, image_rect1.topleft)
    game_display.blit(imageFinal2, image_rect2.topleft)

    #Ligne du sol
    #pygame.draw.rect(game_display, (0, 0, 0), (0, player_y_Baseposition + 40, display_width, 5))

    #Ligne du centre
    #pygame.draw.rect(game_display, (255, 0, 0), (display_width / 2, 0, 1, display_height))

    #Physique rotation bras
    bras_rotatif.theta=bras_rotatif.activer_rotation(keys,pygame.K_LSHIFT)
    bras_rotatif2.theta=bras_rotatif2.activer_rotation(keys,pygame.K_m)

    #Ramasser une boule de neige
    bras_rotatif.ramasser_boule(65,115,game_display,player1)
    bras_rotatif2.ramasser_boule(65,115,game_display,player2)

    #Fermeture de la main
    bras_rotatif.fermer_main(keys,pygame.K_c)
    bras_rotatif2.fermer_main(keys,pygame.K_n)

    #Dessiner la boule
    if bras_rotatif.boule:
        bras_rotatif.dessiner_cercle_main(game_display,player1)
    if bras_rotatif2.boule:
        bras_rotatif2.dessiner_cercle_main(game_display,player2)

    #Rotation bras
    bras_rotatif.posx = player1.position_x
    bras_rotatif.posy = player1.position_y
    bras_rotatif2.posx = player2.position_x
    bras_rotatif2.posy = player2.position_y

    bras_rotatif.tourner_bras(bras_rect,game_display)
    bras_rotatif2.tourner_bras(bras_rect2,game_display)

    #Grossir la boule
    if bras_rotatif.boule_obj is not None:
        bras_rotatif.grossir_boule(65, 115)
    if bras_rotatif2.boule_obj is not None:
        bras_rotatif2.grossir_boule(65, 115)

    #Trajectoire de la boule
    if bras_rotatif.boule_obj is not None and bras_rotatif.boule_obj.lance:
        bras_rotatif.boule_obj.trajectoire_projectile(game_display)
    if bras_rotatif2.boule_obj is not None and bras_rotatif2.boule_obj.lance:
        bras_rotatif2.boule_obj.trajectoire_projectile(game_display)

    #Check collisions de boules
    if bras_rotatif.boule_obj is not None:
        bras_rotatif.boule_obj.check_collision_boule(player2,game_display,menu_de_mort1)
    if bras_rotatif2.boule_obj is not None:
        bras_rotatif2.boule_obj.check_collision_boule(player1,game_display,menu_de_mort2)

    #Obstacles Collisions
    for obstacle in Obstacle_collision:
        obstacle.draw(game_display, (0, 0, 0))  # Draw each obstacle

    # if player1.hitboxe.collidelist(Obstacle_collision) >= 0:
    #     print(player1.hitboxe.collidelist(Obstacle_collision))

    #Les barres
    health1 = Bar(25, 25, 250, 20, 100, player1.pv, "hp")
    health1.draw(game_display)
    health2 = Bar(game_display.get_width() - 275, 25, 250, 20, 100, player2.pv, "hp")
    health2.draw(game_display)
    stamina1 = Bar(25, 55, 250, 20, 200, player1.Stamina, "stamina")
    stamina1.draw(game_display)
    stamina2 = Bar(game_display.get_width() - 275, 55, 250, 20, 200, player2.Stamina, "stamina")
    stamina2.draw(game_display)

    #Décélération
    bras_rotatif.deceleration()
    bras_rotatif2.deceleration()

    #Gestionnaire d'évènements
    for game_event in pygame.event.get():
        if game_event.type == pygame.QUIT:
            menu_principale = False
        if game_event.type == pygame.KEYUP:
            if game_event.key == pygame.K_LSHIFT:
                bras_rotatif.decelerer = True
            if game_event.key == pygame.K_m:
                bras_rotatif2.decelerer = True
            if game_event.key == pygame.K_c:
                bras_rotatif.ouvrir_main()
            if game_event.key == pygame.K_n:
                bras_rotatif2.ouvrir_main()

    pygame.display.update()
    game_clock.tick(60)

pygame.quit()
