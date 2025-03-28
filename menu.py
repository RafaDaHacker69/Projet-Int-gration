import pygame
import time

import Button

class menu:
    def __init__(self, screen):
        self.screen = screen
        self.run = False
        self.restart = False


    def menu(self):
        pygame.mixer.music.load("IMAGES/project2.wav")
        pygame.mixer.music.play(loops=-1, start=0.0)

        width, height = 800, 400
        white = (255, 255, 255)
        black = (0, 0, 0)
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Menu")

        background = pygame.image.load("IMAGES/bg2.png")
        background = pygame.transform.scale(background, (width, height))
        btnJouer = Button.Button((width // 2, height // 4 + 20), "Jouer")
        btnQuitter = Button.Button((width // 2, height // 4 + 176 + 20), "Quitter")
        btnTuto = Button.Button((width // 2, height // 4 + 88 + 20), "Tutoriel")
        clock = pygame.time.Clock()

        shockwaves = []
        running = True
        while running:
            screen.blit(background, (0, 0))
            btnJouer.initialiser(screen)
            btnQuitter.initialiser(screen)
            btnTuto.initialiser(screen)
            btnJouer.verifier(pygame.mouse.get_pos())
            btnQuitter.verifier(pygame.mouse.get_pos())
            btnTuto.verifier(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT or btnQuitter.clique(event, pygame.mouse.get_pos()):
                    running = False
                if btnTuto.clique(event, pygame.mouse.get_pos()):
                    print("tuto")
                if btnJouer.clique(event, pygame.mouse.get_pos()):
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("IMAGES/project 5 final tweak.wav")
                    pygame.mixer.music.play(loops=-1, start=0.0)
                    time.sleep(0.25)
                    self.run = True
                    running = False
                    screen = pygame.display.set_mode((1240, 680))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    shockwaves.append({"x": x, "y": y, "radius": 5, "alpha": 255})

            new_shockwaves = []
            for shockwave in shockwaves:
                shockwave["radius"] += 5
                shockwave["alpha"] -= 15

                if shockwave["alpha"] > 0:
                    new_shockwaves.append(shockwave)

                    circle_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                    pygame.draw.circle(circle_surface, (white[0], white[1], white[2], shockwave["alpha"]),
                                       (shockwave["x"], shockwave["y"]), shockwave["radius"], 2)
                    screen.blit(circle_surface, (0, 0))

            shockwaves = new_shockwaves

            pygame.display.flip()
            clock.tick(60)



    def selection_perso(self,player,bras_rotatif,txt):
        width, height = 1240, 680
        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()


        btn_Joueur_1 = Button.Button((width // 2, height // 4 + 20), "Perso 1")
        btn_Joueur_2 = Button.Button((width // 2, height // 4 + 176 + 20), "Perso 3")
        btn_Joueur_3 = Button.Button((width // 2, height // 4 + 88 + 20), "Perso 2")

        running = True
        while running:
            screen.fill((255, 255, 255))
            font = pygame.font.Font(None, 60)
            text = font.render(txt, True, (0, 0, 0))
            self.screen.blit(text, (400, 75))

            btn_Joueur_1.initialiser(screen)
            btn_Joueur_2.initialiser(screen)
            btn_Joueur_3.initialiser(screen)
            btn_Joueur_1.verifier(pygame.mouse.get_pos())
            btn_Joueur_2.verifier(pygame.mouse.get_pos())
            btn_Joueur_3.verifier(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if btn_Joueur_1.clique(event, pygame.mouse.get_pos()):
                    time.sleep(0.25)
                    running = False
                if btn_Joueur_2.clique(event, pygame.mouse.get_pos()):
                    player.image = pygame.image.load("IMAGES/Cat-removebg.png").convert_alpha()
                    bras_rotatif.alpha = 5
                    bras_rotatif.omega0 = 10
                    time.sleep(0.25)
                    running = False
                if btn_Joueur_3.clique(event, pygame.mouse.get_pos()):
                    player.image = pygame.image.load("IMAGES/Dog-removebg.png").convert_alpha()
                    player.force_saut = 14
                    player.acceleration = 2
                    time.sleep(0.25)
                    running = False

            pygame.display.flip()
            clock.tick(60)


    def menu_mort(self):
        width, height = 1240, 680
        screen = pygame.display.set_mode((width, height))
        retour_menu = Button.Button((width // 2, height // 4 + 20), "Retour au menu")
        clock = pygame.time.Clock()
        running = True
        while running:
            screen.fill((255, 255, 255))
            font = pygame.font.Font(None, 60)
            text = font.render("Bravo vous avez gagné !", True, (0, 0, 0))
            self.screen.blit(text, (400, 75))
            retour_menu.initialiser(screen)
            retour_menu.verifier(pygame.mouse.get_pos())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    time.sleep(0.25)
                    running = False
                    self.menu()
                    self.restart = True
                if retour_menu.clique(event, pygame.mouse.get_pos()):
                    time.sleep(0.25)
                    running = False
                    self.menu()
                    self.restart = True
            pygame.display.flip()
            clock.tick(60)