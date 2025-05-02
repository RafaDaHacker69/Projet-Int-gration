import pygame
from menu import *
from Bar import *
from player import Player
from Bras_Rotatif import Bras_Rotatif
from Obstacle_collision import Obstacle
from Timer import *
import pygame
from PIL import Image


pygame.init()

Width, Height = 1240, 680
width, height = 800, 400
game_display = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Tuto')

BACKGROUND_COLOR = (173, 216, 230)
bg = pygame.image.load('IMAGES/backg.jpg').convert_alpha()
cible = pygame.image.load('IMAGES/cible.png').convert_alpha()
cible =pygame.transform.scale_by(cible, 0.2)
gif_path = 'IMAGES/neige.gif'  # Remplace par le chemin de ton GIF
gif = Image.open(gif_path)

btnMenu = Button.Button((1000,600), "Menu")

font = pygame.font.SysFont(None, 36)

frames = []
try:
    while True:
        frame = pygame.image.fromstring(gif.tobytes(), gif.size, gif.mode)
        frames.append(frame)
        gif.seek(gif.tell() + 1)
except EOFError:
    pass

frame_index = 0
frame_delay = 3
frame_counter = 0

sol = pygame.image.load('IMAGES/sol.png').convert_alpha()
game_clock = pygame.time.Clock()
display_width, display_height = game_display.get_size()

player1 = Player(display_width * 0.2, display_height * 0.8, 30, 40, controles='wasd', pv=75, facteur = 2)
player_image1 = player1.image
player1.last_direction = 1

bras_rotatif = Bras_Rotatif(1, 0, 4, False)
player1.bras_obj = bras_rotatif
bras_rect = bras_rotatif.creation_bras_main(255, 0, 0)

player_y_Baseposition = display_height * 0.88

rect_cible = pygame.Rect(1005,410,85,85)

boucle = True

Obstacle_collision = []
textes = [
    "Bienvenue dans le tutoriel ! (appuie sur ESPACE pour continuer)",
    "Utilise WASD pour te déplacer.",
    "Appuie sur LSHIFT pour faire tourner ton bras !.",
    "Quand le bras du pinguoin est orienté vers le sol, appuie sur C pour former un boule de neige !",
    "Maintenant, relache C pour la lancé !",
    "Ton but sera d'éliminer le joueur adverse avec les boules de neiges",
    "Ton personnage possède de la vie, de l'énergie et une barre de capacité spéciale",
    "Appuie sur Q pour utiliser ta capacité spéciale",
    "Tes PV se sont remontés à 100 !",
    "NB : Chaque personnage à une capacité spéciale différente",
    "Bonne chance !"
]

index_texte = 0

while boucle:



    keys = pygame.key.get_pressed()


    player1.handle_input(keys)
    player1.apply_friction()
    player1.apply_gravity()
    player1.update_position(Obstacle_collision)
    player1.check_ground_collision(player_y_Baseposition)

    if player1.position_x < 0:
        player1.position_x = 0
    if player1.position_x > display_width - 20:
        player1.position_x = display_width - 20

    player1.update_animation()
    frame1 = player1.get_current_frame()

    direction1 = player1.get_movement_direction()

    if player1.last_direction == 1:
        frame1 = pygame.transform.flip(frame1, True, False)
    elif player1.last_direction == -1:
        frame1 = pygame.transform.flip(frame1, False, False)

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

    frame1 = pygame.transform.scale_by(frame1, 0.5)
    rect1 = frame1.get_rect(center=player1.hitboxe.center)
    game_display.blit(frame1, rect1.topleft)

    bras_rotatif.theta = bras_rotatif.activer_rotation(keys, pygame.K_LSHIFT)
    bras_rotatif.ramasser_boule(65, 115, game_display, player1)
    bras_rotatif.fermer_main(keys, pygame.K_c)

    if bras_rotatif.boule:
        bras_rotatif.dessiner_cercle_main(game_display, player1)

    bras_rotatif.posx = player1.position_x
    bras_rotatif.posy = player1.position_y

    bras_rotatif.tourner_bras(bras_rect, game_display)

    if bras_rotatif.boule_obj is not None:
        bras_rotatif.grossir_boule(65, 115)

    if bras_rotatif.boule_obj is not None and bras_rotatif.boule_obj.lance:
        bras_rotatif.boule_obj.trajectoire_projectile(game_display)

    if bras_rotatif.boule_obj is not None:
        rayon = player1.bras_obj.boule_obj.r
        hitboxe = pygame.Rect(player1.bras_obj.boule_obj.x - rayon, player1.bras_obj.boule_obj.y - rayon, rayon * 2, rayon * 2)
        if hitboxe.colliderect(rect_cible):
            player1.bras_obj.boule_obj.lance = False
            player1.bras_obj.boule_obj=None
            print("touché")

    health1 = Bar(25, 25, 250, 20, player1.pv_max, player1.pv, "hp")
    health1.draw(game_display)
    stamina1 = Bar(25, 55, 250, 20, player1.max_Stamina, player1.Stamina, "stamina")
    stamina1.draw(game_display)
    ult1 = Bar(25, 85, 250, 20, player1.charge_max, player1.charge, "ult")
    ult1.draw(game_display)

    bras_rotatif.deceleration()

    btnMenu.initialiser(game_display)
    btnMenu.verifier(pygame.mouse.get_pos())

    pygame.draw.rect(game_display, (139,0,0), rect_cible)
    game_display.blit(cible,(1000,400))

    if index_texte < len(textes):
        texte_surface = font.render(textes[index_texte], True, (255, 255, 255))
        game_display.blit(texte_surface, (50, 300))

    for game_event in pygame.event.get():
        if game_event.type == pygame.QUIT:
            boucle = False
        if game_event.type == pygame.KEYUP:
            if game_event.key == pygame.K_LSHIFT:
                bras_rotatif.decelerer = True
            if game_event.key == pygame.K_c:
                bras_rotatif.ouvrir_main()
            if game_event.key == pygame.K_q:
                player1.ult()
        if game_event.type == pygame.KEYDOWN and game_event.key == pygame.K_SPACE:
            index_texte += 1


    pygame.display.update()
    game_clock.tick(60)
pygame.quit()
