import pygame
import time
import pygame.freetype
import Button

class menu:
    def __init__(self, screen):
        self.screen = screen
        self.run = False
        self.restart = False


    def menu(self):
        pygame.mixer.music.load("IMAGES/10 final.wav")
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
        self.fait=True
        if self.fait :
            texte = " "
            image =pygame.image.load("IMAGES/blank.png").convert_alpha()


        btn_Joueur_1 = Button.Button((width // 2, height // 4 + 20), "Perso 1")
        btn_Joueur_2 = Button.Button((width // 2, height // 4 + 88  + 20), "Perso 2")
        btn_Joueur_3 = Button.Button((width // 2, height // 4 + 176 + 20), "Perso 3")

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
                    bras_rotatif.alpha = 3
                    bras_rotatif.omega0 = 6
                    time.sleep(0.25)
                    running = False
                if btn_Joueur_3.clique(event, pygame.mouse.get_pos()):
                    player.image = pygame.image.load("IMAGES/Dog-removebg.png").convert_alpha()
                    player.force_saut = 14
                    player.acceleration = 2
                    time.sleep(0.25)
                    running = False
                hovered_1 = btn_Joueur_1.rect.collidepoint(pygame.mouse.get_pos())
                hovered_2 = btn_Joueur_2.rect.collidepoint(pygame.mouse.get_pos())
                hovered_3 = btn_Joueur_3.rect.collidepoint(pygame.mouse.get_pos())
                if hovered_1:
                    self.fait=False
                    image = pygame.image.load("IMAGES/finalmodel.png").convert_alpha()
                    texte = "Premier personnage :\n personnage de base avec 100 hp et 200 stamina.\nforce: normale\nvitesse: normale\nsaut:normal\nhabilité ultime : musculature"
                if hovered_2:
                    self.fait = False
                    image = pygame.image.load("IMAGES/Cat-removebg.png").convert_alpha()
                    texte = "Deuxième personnage : \npersonnage rapide avec 100 hp et 200 stamina.\nforce: normale\nvitesse: vite\nsaut: normal\nhabilité ultime : jsp"
                if hovered_3:
                    self.fait = False
                    image = pygame.image.load("IMAGES/Dog-removebg.png").convert_alpha()
                    texte = "Premier personnage :      personnage de base avec 100 hp et 200 stamina.\nforce: normale\nvitesse: normale\nsaut:normal\nhabilité ultime : musculature"
            font = pygame.font.Font(None, 60)
            info = font.render(texte, True, (0, 0, 0))
            self.dessiner_text(self.screen, texte, (25, 175), "IMAGES/grand9k-pixel.ttf", 30, (0, 0, 0), 475)
            self.screen.blit(image, (800, 75))
            pygame.display.flip()
            clock.tick(60)

    def dessiner_text(self, screen, text, position, font, taille, couleur, wrap):
        pygame.freetype.init()
        font = pygame.freetype.Font(font, taille)

        lignes = []
        for ligne in text.splitlines():
            mots = ligne.split()
            ligneCourante = ""

            for mot in mots:
                lignesTemp = ligneCourante + " " + mot if ligneCourante else mot
                if font.get_rect(lignesTemp).width <= wrap:
                    ligneCourante = lignesTemp
                else:
                    lignes.append(ligneCourante)
                    ligneCourante = mot
            lignes.append(ligneCourante)

        x, y = position
        espace = taille + 5
        for ligne in lignes:
            font.render_to(screen, (x, y), ligne, couleur)
            y += espace

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