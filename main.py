import pygame
from player import Player

pygame.init()

game_display = pygame.display.set_mode((1240, 680))
game_clock = pygame.time.Clock()

BACKGROUND_COLOR = pygame.Color('white')
display_width, display_height = game_display.get_size()

player1 = Player(display_width * 0.2, display_height * 0.8, 30, 40, controls='wasd')
player2 = Player(display_width * 0.7, display_height * 0.8, 30, 40, controls='arrows')

player_y_Baseposition = display_height * 0.8

game_running = True
while game_running:
    for game_event in pygame.event.get():
        if game_event.type == pygame.QUIT:
            game_running = False

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
    elif player1.x_position + player1.width > display_width / 2:  # Prevents clipping
        player1.x_position = display_width / 2 - player1.width

    if player2.x_position > display_width - 20:
        player2.x_position = display_width - 20
    elif player2.x_position < display_width / 2:
        player2.x_position = display_width / 2

    # Rendu graphique
    game_display.fill(BACKGROUND_COLOR)

    player1.draw(game_display, (0, 120, 250))
    player2.draw(game_display, (255, 0, 0))

    pygame.draw.rect(game_display, (0, 0, 0), (0, player_y_Baseposition + 40, display_width, 5))
    pygame.draw.rect(game_display, (255, 0, 0), (display_width / 2, 0, 1, display_height))

    pygame.display.update()

    game_clock.tick(60)

pygame.quit()
