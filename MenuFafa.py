import pygame


import Button

class MenuFafa:
    def __init__(self, screen):
        self.screen = screen
        self.run = False


    def MenuFafa(self):
        pygame.mixer.music.load("IMAGES/project2.wav")
        pygame.mixer.music.play(loops=-1, start=0.0)

        width, height = 800, 400
        white = (255, 255, 255)
        black = (0, 0, 0)
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Example Menu")

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



    def selection_perso(self,player,bras_rotatif):

        width, height = 800, 400
        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()

        btn_Joueur_1 = Button.Button((width // 2, height // 4 + 20), "Perso 1")
        btn_Joueur_2 = Button.Button((width // 2, height // 4 + 176 + 20), "Perso 2")
        btn_Joueur_3 = Button.Button((width // 2, height // 4 + 88 + 20), "Perso 3")

        running = True
        while running:
            btn_Joueur_1.initialiser(screen)
            btn_Joueur_2.initialiser(screen)
            btn_Joueur_3.initialiser(screen)
            btn_Joueur_1.verifier(pygame.mouse.get_pos())
            btn_Joueur_2.verifier(pygame.mouse.get_pos())
            btn_Joueur_3.verifier(pygame.mouse.get_pos())



            screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if btn_Joueur_1.clique(event, pygame.mouse.get_pos()):
                    running = False
                if btn_Joueur_2.clique(event, pygame.mouse.get_pos()):
                    bras_rotatif.alpha = 5
                    bras_rotatif.omega = 10
                    running = False
                if btn_Joueur_3.clique(event, pygame.mouse.get_pos()):
                    player.force_saut = 14
                    player.acceleration = 2
                    running = False

            pygame.display.flip()
            clock.tick(60)