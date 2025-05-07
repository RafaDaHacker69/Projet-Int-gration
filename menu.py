import pygame.freetype
import Button
from tuto import *
import time
from PIL import Image
import threading


class menu:
    def __init__(self, screen):
        self.screen = screen
        self.run = False
        self.restart = False
        self.choisi=False
        self.tuto = False
        self.quitter = False

    def charger_sprite_sheet(self, chemin, lignes, colonnes):
        sheet = pygame.image.load(chemin).convert_alpha()
        frames = []
        sheet_width, sheet_height = sheet.get_size()
        frame_width = sheet_width // colonnes
        frame_height = sheet_height // lignes
        for i in range(lignes):
            for j in range(colonnes):
                frame = sheet.subsurface(pygame.Rect(j * frame_width, i * frame_height, frame_width, frame_height))
                frames.append(frame)
        return frames

    def menu(self):
        pygame.mixer.music.load("IMAGES/project 9 DRAFT.wav")
        pygame.mixer.music.play(loops=-1, start=0.0)

        width, height = 800, 400
        white = (255, 255, 255)
        black = (0, 0, 0)
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Menu")

        gif_path = 'IMAGES/bg anim2.gif'
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
        frame_index = 0
        frame_delay = 5
        frame_counter = 0


        background = pygame.image.load("IMAGES/bg2.png")
        background = pygame.transform.scale(background, (width, height))
        btnJouer = Button.Button((width // 2, height // 4 + 20), "Jouer")
        btnQuitter = Button.Button((width // 2, height // 4 + 176 + 20), "Quitter")
        btnTuto = Button.Button((width // 2, height // 4 + 88 + 20), "Tutoriel")
        clock = pygame.time.Clock()

        shockwaves = []
        running = True
        while running:
            screen.blit(frames[frame_index], (0, 0))
            frame_counter += 1
            if frame_counter >= frame_delay:
                frame_counter = 0
                # Si on est sur la dernière frame, revenir à la première frame
                if frame_index == len(frames) - 1:
                    frame_index = 1
                else:
                    frame_index += 1  # Passer à la frame suivante
            btnJouer.initialiser(screen)
            btnQuitter.initialiser(screen)
            btnTuto.initialiser(screen)
            btnJouer.verifier(pygame.mouse.get_pos())
            btnQuitter.verifier(pygame.mouse.get_pos())
            btnTuto.verifier(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT or btnQuitter.clique(event, pygame.mouse.get_pos()):
                    running = False
                    self.quitter = True
                if btnTuto.clique(event, pygame.mouse.get_pos()):
                    print("tuto")
                    self.tuto = True
                    running = False
                    screen = pygame.display.set_mode((1240, 680))
                if btnJouer.clique(event, pygame.mouse.get_pos()):
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

        black_frames = self.charger_sprite_sheet("IMAGES/Menu idle black.png", 1, 20)
        red_frames = self.charger_sprite_sheet("IMAGES/Menu idle red.png", 1, 20)
        blue_frames = self.charger_sprite_sheet("IMAGES/Menu idle blue.png", 1, 20)

        frame_delay_2 = 5
        frame_index_2 = 0
        frame_counter_2 = 0

        current_frames = None  # To store the active hover animation

        btn_Joueur_1 = Button.Button((width // 2, height // 4 + 20), "Perso 1")
        btn_Joueur_2 = Button.Button((width // 2, height // 4 + 88  + 20), "Perso 2")
        btn_Joueur_3 = Button.Button((width // 2, height // 4 + 176 + 20), "Perso 3")

        running = True
        while running:
            screen.fill((255, 255, 255))
            font = pygame.font.Font("IMAGES/grand9k-pixel.ttf", 50)
            text = font.render(txt, True, (0, 0, 0))
            self.screen.blit(text, (320, 25))
            btn_Joueur_1.initialiser(screen)
            btn_Joueur_2.initialiser(screen)
            btn_Joueur_3.initialiser(screen)
            btn_Joueur_1.verifier(pygame.mouse.get_pos())
            btn_Joueur_2.verifier(pygame.mouse.get_pos())
            btn_Joueur_3.verifier(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quitter = True
                    sys.exit()
                if btn_Joueur_1.clique(event, pygame.mouse.get_pos()):
                    player.load_sprite_sheet("IMAGES/final model-Sheet(black).png", 10)
                    player.load_idle_sprite_sheet("IMAGES/idle_black.png", 28)
                    player.facteur=0.03
                    time.sleep(0.25)
                    self.choisi = True
                    running = False
                if btn_Joueur_2.clique(event, pygame.mouse.get_pos()):
                    player.load_sprite_sheet("IMAGES/final model-Sheet(red).png", 10)
                    player.load_idle_sprite_sheet("IMAGES/idle_red.png", 28)
                    player.joueurSorte=2
                    player.pv = 80
                    player.pv_max = 80
                    player.facteur=0.01
                    bras_rotatif.alpha = 2
                    bras_rotatif.omega0 = 5
                    time.sleep(0.25)
                    self.choisi = True
                    running = False
                if btn_Joueur_3.clique(event, pygame.mouse.get_pos()):
                    player.load_sprite_sheet("IMAGES/final model-Sheet(blue).png", 10)
                    player.load_idle_sprite_sheet("IMAGES/idle_blue.png", 28)
                    player.joueurSorte = 3
                    player.Stamina=120
                    player.max_Stamina=120
                    player.pv = 1
                    player.pv_max = 90
                    player.facteur=0.02
                    player.force_saut = 11
                    player.acceleration = 2
                    time.sleep(0.25)
                    self.choisi=True
                    running = False
                hovered_1 = btn_Joueur_1.rect.collidepoint(pygame.mouse.get_pos())
                hovered_2 = btn_Joueur_2.rect.collidepoint(pygame.mouse.get_pos())
                hovered_3 = btn_Joueur_3.rect.collidepoint(pygame.mouse.get_pos())

                if hovered_1:
                    current_frames = black_frames
                    texte = "Premier personnage :\npersonnage de base avec 100 hp et 100 stamina.\nforce: normale\nvitesse: normale\nsaut:normal\nhabilité ultime : regénération de santé"
                elif hovered_2:
                    current_frames = red_frames
                    texte = "Deuxième personnage :\npersonnage agressif avec 80 hp et 100 stamina.\nforce: fort\nvitesse: normal\nsaut: normal\nhabilité ultime : boule de feu"
                elif hovered_3:
                    current_frames = blue_frames
                    texte = "Troisième personnage :\npersonnage mobile avec 90 hp et 120 stamina.\nforce: normale\nvitesse: vite\nsaut:élevé\nhabilité ultime : construction de mur"
                else:
                    current_frames = None
                    font = pygame.font.Font(None, 60)

            if current_frames:
                frame_counter_2 += 1
                if frame_counter_2 >= frame_delay_2:
                    frame_counter_2 = 0
                    frame_index_2 = (frame_index_2 + 1) % len(current_frames)

                frame_image = current_frames[frame_index_2]
                frame_image = pygame.transform.smoothscale(frame_image, (
                int(frame_image.get_width() * 1.5), int(frame_image.get_height() * 1.5)))
                screen.blit(frame_image,
                            (width - frame_image.get_width() - 50, height // 2 - frame_image.get_height() // 2))

            info = font.render(texte, True, (0, 0, 0))
            self.dessiner_text(self.screen, texte, (25, 175), "IMAGES/grand9k-pixel.ttf", 30, (0, 0, 0), 475)
            imageFinale = pygame.transform.smoothscale(image,(int(image.get_width() * 1.5), int(image.get_height() * 1.5)))
            self.screen.blit(imageFinale, (800, 125))
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

    def menu_mort(self, nbJoueur,playerSorte):
        width, height = 1240, 680
        screen = pygame.display.set_mode((width, height))
        pygame.mixer.music.stop()
        pygame.mixer.music.load("IMAGES/win music.wav")
        pygame.mixer.music.play(loops=-1, start=0.0)
        gif_path = 'IMAGES/winBlack.gif'
        if playerSorte==2:
            gif_path = 'IMAGES/winRed.gif'
        if playerSorte==3:
            gif_path = 'IMAGES/winBlue.gif'
        gif = Image.open(gif_path)
        frames = []

        def extract_gif_frames():
            try:
                while True:
                    frame = pygame.image.fromstring(gif.tobytes(), gif.size, gif.mode)
                    frame = pygame.transform.scale(frame, (width, height))  # scale to screen size
                    frames.append(frame)
                    gif.seek(gif.tell() + 1)
            except EOFError:
                pass

        extract_gif_frames()

        frame_index = 0
        frame_delay = 5
        frame_counter = 0

        retour_menu = Button.Button((width // 2, height // 4 + 20), "Retour")
        clock = pygame.time.Clock()
        running = True

        while running:
            if frames:
                screen.blit(frames[frame_index], (0, 0))

                frame_counter += 1
                if frame_counter >= frame_delay:
                    frame_counter = 0
                    frame_index = (frame_index + 1) % len(frames)

            font = pygame.font.Font(None, 60)
            txt = "Victoire du joueur " + str(nbJoueur) + "!"
            text = font.render(txt, True, (0, 0, 0))
            self.screen.blit(text, (400, 75))

            retour_menu.initialiser(screen)
            retour_menu.verifier(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    time.sleep(0.25)
                    running = False
                    self.restart = True
                if retour_menu.clique(event, pygame.mouse.get_pos()):
                    time.sleep(0.25)
                    running = False
                    self.restart = True

            pygame.display.flip()
            clock.tick(60)
