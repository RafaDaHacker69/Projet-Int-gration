from menu import *
from Bar import *
from player import Player
from Bras_Rotatif import Bras_Rotatif
from Obstacle_collision import Obstacle
from Timer import *
import pygame
from PIL import Image

restart = False

def jeu(): #fortnite
    global restart
    pygame.init()

    Width, Height = 1240, 680
    facteurDegat=1
    jouerMusique=True
    recommence=True

    game_display = pygame.display.set_mode((Width, Height))
    menu_display = pygame.display.set_mode((1, 1))
    pygame.display.set_caption('CP (Club Penguin)')

    menu_principale = menu(menu_display)
    menu_principale.menu()

    game_clock = pygame.time.Clock()

    timer = Timer(300, 50, Width / 2 - 100, 25, (255, 255, 255), game_display)


    BACKGROUND_COLOR = pygame.Color('white')
    #bg = pygame.image.load('IMAGES/neige.gif').convert_alpha()
    gif_path = 'IMAGES/neige-2.gif'  # Remplace par le chemin de ton GIF
    gif = Image.open(gif_path)

    frames = []
    try:
        while True:
            frame = pygame.image.fromstring(gif.tobytes(), gif.size, gif.mode)
            frames.append(frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    frame_index = 0

    sol = pygame.image.load('IMAGES/sol.png').convert_alpha()
    display_width, display_height = game_display.get_size()

    player1 = Player(display_width * 0.2, display_height * 0.8, 30, 40, controles='wasd')
    player2 = Player(display_width * 0.7, display_height * 0.8, 30, 40, controles='fleches')

    bras_rotatif = Bras_Rotatif(1, 0, 4, False)
    bras_rotatif2 = Bras_Rotatif(1, 0, 4, True)

    menu_perso1 = menu(menu_display)
    menu_perso1.selection_perso(player1, bras_rotatif, "Sélection du Joueur 1")

    menu_perso2 = menu(menu_display)
    menu_perso2.selection_perso(player2, bras_rotatif2, "Sélection du Joueur 2")

    menu_de_mort1 = menu(menu_display)
    menu_de_mort2 = menu(menu_display)

    player_image1 = player1.image
    player_image2 = player2.image
    player1_image_flip = pygame.transform.flip(player_image1, True, False)
    player2_image_flip = pygame.transform.flip(player_image2, False, False)

    bras_rect = bras_rotatif.creation_bras_main(255, 0, 0)
    bras_rect2 = bras_rotatif2.creation_bras_main(0, 120, 250)

    player_y_Baseposition = display_height * 0.88

    Obstacle_collision = [
        Obstacle(100, display_height - 90, 50, 50),
        Obstacle(120, display_height - 100, 50, 50),
        Obstacle(140, display_height - 110, 50, 50),
        Obstacle(160, display_height - 100, 50, 50),
        Obstacle(180, display_height - 90, 50, 50),
        Obstacle(320, display_height - 200, 50, 100),
    ]

    while menu_principale.run:

        keys = pygame.key.get_pressed()

        for player in (player1, player2):
            player.handle_input(keys)
            player.apply_friction()
            player.apply_gravity()
            player.update_position(Obstacle_collision)
            player.check_ground_collision(player_y_Baseposition)

        if player1.position_x < 0:
            player1.position_x = 0
        elif player1.position_x + player1.largeur > display_width / 2:
            player1.position_x = display_width / 2 - player1.largeur

        if player2.position_x > display_width - 20:
            player2.position_x = display_width - 20
        elif player2.position_x < display_width / 2:
            player2.position_x = display_width / 2

        direction1 = player1.get_movement_direction()
        direction2 = player2.get_movement_direction()

        if direction1 == "right":
            player1_image_flip = pygame.transform.flip(player_image1, True, False)
        elif direction1 == "left":
            player1_image_flip = pygame.transform.flip(player_image1, False, False)

        if direction2 == "right":
            player2_image_flip = pygame.transform.flip(player_image2, True, False)
        elif direction2 == "left":
            player2_image_flip = pygame.transform.flip(player_image2, False, False)

        game_display.fill(BACKGROUND_COLOR)
        game_display.blit(frames[frame_index], (0, 0))
        frame_index = (frame_index + 1) % len(frames)
        #game_display.blit(bg, (0, 0))
        game_display.blit(sol, (0, 585))

        player1.hitboxes(game_display)
        player2.hitboxes(game_display)

        imageFinal1 = pygame.transform.scale_by(player1_image_flip, 0.4)
        image_rect1 = imageFinal1.get_rect(center=player1.hitboxe.center)
        imageFinal2 = pygame.transform.scale_by(player2_image_flip, 0.4)
        image_rect2 = imageFinal2.get_rect(center=player2.hitboxe.center)

        game_display.blit(imageFinal1, image_rect1.topleft)
        game_display.blit(imageFinal2, image_rect2.topleft)

        bras_rotatif.theta = bras_rotatif.activer_rotation(keys, pygame.K_LSHIFT)
        bras_rotatif2.theta = bras_rotatif2.activer_rotation(keys, pygame.K_m)

        bras_rotatif.ramasser_boule(65, 115, game_display, player1)
        bras_rotatif2.ramasser_boule(65, 115, game_display, player2)

        bras_rotatif.fermer_main(keys, pygame.K_c)
        bras_rotatif2.fermer_main(keys, pygame.K_n)

        if bras_rotatif.boule:
            bras_rotatif.dessiner_cercle_main(game_display, player1)
        if bras_rotatif2.boule:
            bras_rotatif2.dessiner_cercle_main(game_display, player2)

        bras_rotatif.posx = player1.position_x
        bras_rotatif.posy = player1.position_y
        bras_rotatif2.posx = player2.position_x
        bras_rotatif2.posy = player2.position_y

        bras_rotatif.tourner_bras(bras_rect, game_display)
        bras_rotatif2.tourner_bras(bras_rect2, game_display)

        if bras_rotatif.boule_obj is not None:
            bras_rotatif.grossir_boule(65, 115)
        if bras_rotatif2.boule_obj is not None:
            bras_rotatif2.grossir_boule(65, 115)

        if bras_rotatif.boule_obj is not None and bras_rotatif.boule_obj.lance:
            bras_rotatif.boule_obj.trajectoire_projectile(game_display)
        if bras_rotatif2.boule_obj is not None and bras_rotatif2.boule_obj.lance:
            bras_rotatif2.boule_obj.trajectoire_projectile(game_display)

        if bras_rotatif.boule_obj is not None:
            bras_rotatif.boule_obj.check_collision_boule(player2, game_display, menu_de_mort1,player1,facteurDegat)
        if bras_rotatif2.boule_obj is not None:
            bras_rotatif2.boule_obj.check_collision_boule(player1, game_display, menu_de_mort2,player2,facteurDegat)

        for obstacle in Obstacle_collision:
            obstacle.draw(game_display, (0, 0, 0))

        # Le temps
        if (menu_perso2.choisi):
            if (recommence):
                pygame.mixer.music.stop()
                pygame.mixer.music.load("IMAGES/project 5 final tweak.wav")
                pygame.mixer.music.play(loops=-1, start=0.0)
                timer.reset()
                recommence=False
            timer.draw()
            timer.update()
            if (timer.secs - timer.getTemps() <= 60):
                player1.facteur = 0.08
                player2.facteur = 0.08
                if jouerMusique:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("IMAGES/project 11 DRAFT.wav")
                    pygame.mixer.music.play(loops=-1, start=0.0)
                    jouerMusique = False
            if (timer.is_finished()):
                if player1.pv < player2.pv:
                    menu_de_mort1.menu_mort()

                if player1.pv > player2.pv:
                    menu_de_mort2.menu_mort()

        health1 = Bar(25, 25, 250, 20, player1.pv_max, player1.pv, "hp")
        health1.draw(game_display)
        health2 = Bar(game_display.get_width() - 275, 25, 250, 20, player2.pv_max, player2.pv, "hp")
        health2.draw(game_display)
        stamina1 = Bar(25, 55, 250, 20, player1.max_Stamina, player1.Stamina, "stamina")
        stamina1.draw(game_display)
        stamina2 = Bar(game_display.get_width() - 275, 55, 250, 20, player1.max_Stamina, player2.Stamina, "stamina")
        stamina2.draw(game_display)
        ult1 = Bar(25, 85, 250, 20, player1.charge_max, player1.charge, "ult")
        ult1.draw(game_display)
        ult2 = Bar(game_display.get_width() - 275, 85, 250, 20, player2.charge_max, player2.charge, "ult")
        ult2.draw(game_display)

        bras_rotatif.deceleration()
        bras_rotatif2.deceleration()

        if menu_de_mort1.restart or menu_de_mort2.restart:
            restart = True
            return

        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                menu_principale.run = False
            if game_event.type == pygame.KEYUP:
                if game_event.key == pygame.K_LSHIFT:
                    bras_rotatif.decelerer = True
                if game_event.key == pygame.K_m:
                    bras_rotatif2.decelerer = True
                if game_event.key == pygame.K_c:
                    bras_rotatif.ouvrir_main()
                if game_event.key == pygame.K_n:
                    bras_rotatif2.ouvrir_main()
                if game_event.key == pygame.K_q:
                    player1.ult()
                if game_event.key == pygame.K_p:
                    player2.ult()

        pygame.display.update()
        game_clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    while True:
        restart = False
        jeu()
        if not restart:
            break