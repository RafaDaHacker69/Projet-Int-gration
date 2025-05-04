import pygame
import sys
import threading

class LoadingScreen:
    def __init__(self):
        self.loading_finished = False
        self.loading_progress = 0

    def loading(self):
        pygame.init()
        screen = pygame.display.set_mode((1240, 680))
        pygame.display.set_caption("Chargement")
        clock = pygame.time.Clock()

        work = 100000000

        font = pygame.font.Font("IMAGES/grand9k-pixel.ttf", 50)
        text = font.render("Chargement...", True, (0,0,0))


        loading_bg = pygame.image.load('IMAGES/Loading Bar Background.png')
        loading_rect = loading_bg.get_rect(center=(620, 440))

        loading_bar_original = pygame.image.load('IMAGES/Loading Bar.png')
        loading_bar_rect = loading_bar_original.get_rect(midleft=(260, 440))

        def doWork():
            for i in range(work):
                _ = 52367 / 42356435 * 23452342  # simulé
                self.loading_progress = i
            self.loading_finished = True

        threading.Thread(target=doWork).start()

        tips = [
            "Bienvenue dans le tutoriel ! (appuie sur ESPACE pour continuer)",
            "Utilise WASD pour te déplacer.",
            "Appuie sur LSHIFT pour faire tourner ton bras !",
            "Quand le bras du pinguoin est orienté vers le sol, appuie sur C pour former un boule de neige !",
            "Maintenant, relache C pour la lancé !",
            "Ton but sera d'éliminer le joueur adverse avec les boules de neiges",
            "Pratique toi sur la cible",
            "Ton personnage possède de la vie, de l'énergie et une barre de capacité spéciale",
            "Appuie sur Q pour utiliser ta capacité spéciale",
            "Tes PV se sont remontés à 100 !",
            "NB : Chaque personnage à une capacité spéciale différente",
            "Bonne chance !"
        ]
        index_texte = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    index_texte += 1
            screen.fill((160, 200, 220))  # RGB de "#0d0e2e"

            if not self.loading_finished:
                progress_ratio = self.loading_progress / work
                loading_bar_width = max(1, int(progress_ratio * 720))

                loading_bar = pygame.transform.scale(loading_bar_original, (loading_bar_width, 150))
                loading_bar_rect = loading_bar.get_rect(midleft=(260, 440))

                screen.blit(text,(440,250))
                screen.blit(loading_bg, loading_rect)
                screen.blit(loading_bar, loading_bar_rect)
            else:
                print("Chargement terminé !")
                break

            if index_texte < len(tips):
                texte_surface = font.render(tips[index_texte], True, (255, 255, 255))
                screen.blit(texte_surface, (50, 300))

            pygame.display.update()
            clock.tick(60)


