from menu import *
from Bar import *
from Obstacle_collision import *
from player import Player
from Bras_Rotatif import Bras_Rotatif
from Timer import *
from PIL import Image
from Loading_Screen import *
import threading
from Button import *

restart = False

def jeu():
    global restart
    pygame.init()

    Width, Height = 1240, 680
    jouerMusique=True
    recommence=True

    game_display = pygame.display.set_mode((Width, Height))
    menu_display = pygame.display.set_mode((1, 1))

    menu_principale = menu(menu_display)
    menu_principale.menu()

    menu_de_mort1 = menu(menu_display)
    menu_de_mort2 = menu(menu_display)

    if menu_principale.quitter:
        pygame.quit()
        sys.exit()

    tuto = Tuto()

    game_clock = pygame.time.Clock()
    timer = Timer(180, 50, Width / 2 - 100, 25, (255, 255, 255), game_display)

    BACKGROUND_COLOR = (173, 216, 230)
    loading = LoadingScreen()

    bg = pygame.image.load('IMAGES/backg.jpg').convert_alpha()
    gif_path = 'IMAGES/anim neige(REAL).gif'
    gif = Image.open(gif_path)

    frames = []
    def gerer_gif():
        try:
            while True:
                frame = pygame.image.fromstring(gif.tobytes(), gif.size, gif.mode)
                frames.append(frame)
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
    threading.Thread(target=gerer_gif).start()

    if menu_principale.tuto:
        tuto.tutoriel()
        restart = True
        


    frame_index = 0
    frame_delay = 3
    frame_counter = 0

    sol = pygame.image.load('IMAGES/sol.png').convert_alpha()
    display_width, display_height = game_display.get_size()

    player1 = Player(display_width * 0.2, display_height * 0.8, 30, 40, controles='wasd', pv=100,inverse=False)
    player2 = Player(display_width * 0.7, display_height * 0.8, 30, 40, controles='fleches', pv=100,inverse=True)
    player2.nbJoueur = 2
    player1.last_direction = 1  # Facing right
    player2.last_direction = -1  # Facing left

    bras_rotatif = Bras_Rotatif(1, 0, 4, False)
    bras_rotatif2 = Bras_Rotatif(1, 0, 4, True)

    player1.bras_obj = bras_rotatif
    player2.bras_obj = bras_rotatif2

    if not restart:
        loading.loading()
        menu_perso1 = menu(menu_display)
        menu_perso1.selection_perso(player1, bras_rotatif, "Sélection du Joueur 1")
        menu_perso2 = menu(menu_display)
        menu_perso2.selection_perso(player2, bras_rotatif2, "Sélection du Joueur 2")

    pygame.display.set_caption('CP (Club Penguin)')

    # player_image1 = player1.image
    # player_image2 = player2.image

    # player1_image_flip = pygame.transform.flip(player_image1, True, False)
    # player2_image_flip = pygame.transform.flip(player_image2, False, False)

    bras_rect = bras_rotatif.creation_bras_main(255, 0, 0)
    bras_rect2 = bras_rotatif2.creation_bras_main(0, 120, 250)

    player_y_Baseposition = display_height * 0.88

    Obstacle_collision = [
        # Obstacle(100, display_height - 90, 50, 50),
    ]
    block_width = 5
    block_height = 120
    for x in range(0, display_width, block_width):
        y = display_height-120
        Obstacle_collision.append(Obstacle(x, y, block_width, block_height))
        #print("block created")

    def is_close_to_obstacle_beneath(player, obstacles, max_y_distance=15):
        px = player.hitboxe.centerx
        py = player.hitboxe.bottom

        closest_obstacle = None
        min_distance = float('inf')

        for obstacle in obstacles:
            ox = obstacle.rect.centerx
            oy = obstacle.rect.top

            if obstacle.rect.collidepoint(px, oy):  # Ensure it's aligned horizontally
                y_distance = oy - py
                if 0 <= y_distance < min_distance:
                    min_distance = y_distance
                    closest_obstacle = obstacle

        return min_distance <= max_y_distance

    def shrink_obstacle_under_player_area(player, obstacles, max_radius=40, max_shrink=3):
        px = player.hitboxe.centerx
        py = player.hitboxe.bottom + 1

        for obstacle in obstacles:
            if abs(obstacle.rect.centery - py) < max_radius * 2:
                cx = obstacle.rect.centerx
                distance = abs(cx - px)

                if distance <= max_radius:
                    factor = 1 - (distance / max_radius)
                    shrink_amount = max_shrink * factor

                    if obstacle.taille_y > 0:
                        obstacle.taille_y -= shrink_amount
                        if obstacle.taille_y < 0:
                            obstacle.taille_y = 0
                        obstacle.rect.y = obstacle.original_y + (obstacle.original_height - obstacle.taille_y)
                        obstacle.rect.height = obstacle.taille_y
                        player.position_y = obstacle.rect.top - player.hauteur
                        if player.on_ground:
                            player.on_ground = False

    mur1_real = True
    mur2_real = True

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

        player1.update_animation()
        player2.update_animation()

        frame1 = player1.get_current_frame()
        frame2 = player2.get_current_frame()

        direction1 = player1.get_movement_direction()
        direction2 = player2.get_movement_direction()

        if player1.last_direction == 1:
            frame1 = pygame.transform.flip(frame1, True, False)
        elif player1.last_direction == -1:
            frame1 = pygame.transform.flip(frame1, False, False)

        if player2.last_direction == 1:
            frame2 = pygame.transform.flip(frame2, True, False)
        elif player2.last_direction == -1:
            frame2 = pygame.transform.flip(frame2, False, False)

        game_display.fill(BACKGROUND_COLOR)
        game_display.blit(bg, (0, 0))
        game_display.blit(frames[frame_index], (0, 0))
        frame_counter += 1
        if frame_counter >= frame_delay:
            frame_counter = 0
            # Si on est sur la dernière frame, revenir à la première frame
            if frame_index == len(frames) - 1:
                frame_index = 1
            else:
                frame_index += 1  # Passer à la frame suivante


        game_display.blit(sol, (0, 585))

        player1.hitboxes(game_display)
        player2.hitboxes(game_display)

        frame1 = pygame.transform.scale_by(frame1, 0.5)
        frame2 = pygame.transform.scale_by(frame2, 0.5)

        rect1 = frame1.get_rect(center=player1.hitboxe.center)
        rect2 = frame2.get_rect(center=player2.hitboxe.center)

        game_display.blit(frame1, rect1.topleft)
        game_display.blit(frame2, rect2.topleft)

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

        bras_rotatif.tourner_bras(bras_rect, game_display,player1.joueurSorte)
        bras_rotatif2.tourner_bras(bras_rect2, game_display,player2.joueurSorte)

        if bras_rotatif.boule_obj is not None:
            if not is_close_to_obstacle_beneath(player1, Obstacle_collision):
                if bras_rotatif.grossir_boule(50, 125, player1):
                    shrink_obstacle_under_player_area(player1, Obstacle_collision)
        if bras_rotatif2.boule_obj is not None:
            if not is_close_to_obstacle_beneath(player2, Obstacle_collision):
                if bras_rotatif2.grossir_boule(50, 125, player2):
                    shrink_obstacle_under_player_area(player2, Obstacle_collision)

        if bras_rotatif.boule_obj is not None and bras_rotatif.boule_obj.lance:
            bras_rotatif.boule_obj.trajectoire_projectile(game_display, Obstacle_collision,player1)
        if bras_rotatif2.boule_obj is not None and bras_rotatif2.boule_obj.lance:
            bras_rotatif2.boule_obj.trajectoire_projectile(game_display, Obstacle_collision,player2)

        if bras_rotatif.boule_obj is not None:
            bras_rotatif.boule_obj.check_collision_boule(player2, game_display, menu_de_mort1,player1)
        if bras_rotatif2.boule_obj is not None:
            bras_rotatif2.boule_obj.check_collision_boule(player1, game_display, menu_de_mort2,player2)

        # if bras_rotatif.boule_obj is not None:
        #     bras_rotatif.ralentissement_boule()
        # if bras_rotatif2.boule_obj is not None:
        #     bras_rotatif2.ralentissement_boule()

        for obstacle in Obstacle_collision:
            players_on_obstacle = any(obstacle.is_player_on_top(player) for player in [player1, player2])
            if not players_on_obstacle:
                obstacle.regrow()
            obstacle.draw(game_display, (255, 255, 255))

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
                    pygame.mixer.music.load("IMAGES/project 11(final).wav")
                    pygame.mixer.music.play(loops=-1, start=0.0)
                    jouerMusique = False
            if (timer.is_finished()):
                if player1.pv < player2.pv:
                    menu_de_mort1.menu_mort("2",player2.joueurSorte)

                if player1.pv > player2.pv:
                    menu_de_mort2.menu_mort("1",player1.joueurSorte)

        health1 = Bar(25, 25, 250, 20, player1.pv_max, player1.pv, "hp")
        health1.draw(game_display)
        health2 = Bar(game_display.get_width() - 275, 25, 250, 20, player2.pv_max, player2.pv, "hp")
        health2.draw(game_display)
        stamina1 = Bar(25, 55, 250, 20, player1.max_Stamina, player1.Stamina, "stamina")
        stamina1.draw(game_display)
        stamina2 = Bar(game_display.get_width() - 275, 55, 250, 20, player2.max_Stamina, player2.Stamina, "stamina")
        stamina2.draw(game_display)
        ult1 = Bar(25, 85, 250, 20, player1.charge_max, player1.charge, "ult")
        ult1.draw(game_display)
        ult2 = Bar(game_display.get_width() - 275, 85, 250, 20, player2.charge_max, player2.charge, "ult")
        ult2.draw(game_display)

        bras_rotatif.deceleration()
        bras_rotatif2.deceleration()

        if player1.mur :
            if mur1_real:
                mur1 = Obstacle(player1.position_x_mur, player1.position_y_mur, 30, 120)
                Obstacle_collision.append(mur1)
                mur1_real = False
            mur1.draw(game_display,(255,255,255))
            if bras_rotatif2.boule_obj is not None:
                bras_rotatif2.boule_obj.check_collision_mur(mur1)
                if bras_rotatif2.boule_obj.mur_brise :
                    Obstacle_collision.remove(mur1)
                    bras_rotatif2.boule_obj.mur_brise = False
                    mur1_real = True
                    player1.mur = False

        if player2.mur:
            if mur2_real:
                mur2 = Obstacle(player2.position_x_mur, player2.position_y_mur, 30, 120)
                Obstacle_collision.append(mur2)
                mur2_real = False
            mur2.draw(game_display, (255, 255, 255))
            if bras_rotatif.boule_obj is not None:
                bras_rotatif.boule_obj.check_collision_mur(mur2)
                if bras_rotatif.boule_obj.mur_brise :
                    Obstacle_collision.remove(mur2)
                    bras_rotatif.boule_obj.mur_brise = False
                    mur2_real = True
                    player2.mur = False

        if bras_rotatif.boule_obj is not None and bras_rotatif.boule_obj.collision:
            bras_rotatif.boule_obj = None
        if bras_rotatif2.boule_obj is not None and bras_rotatif2.boule_obj.collision:
            bras_rotatif2.boule_obj = None

        player1.reset_ulti_dmg()
        player2.reset_ulti_dmg()

        #print(player1.ulti_dmg)

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