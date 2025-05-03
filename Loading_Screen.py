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

        loading_bg = pygame.image.load('IMAGES/Loading Bar Background.png')
        loading_rect = loading_bg.get_rect(center=(620, 340))

        loading_bar_original = pygame.image.load('IMAGES/Loading Bar.png')
        loading_bar_rect = loading_bar_original.get_rect(midleft=(280, 340))

        def doWork():
            for i in range(work):
                _ = 52367 / 42356435 * 23452342  # simulé
                self.loading_progress = i
            self.loading_finished = True

        threading.Thread(target=doWork).start()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill((13, 14, 46))  # RGB de "#0d0e2e"

            if not self.loading_finished:
                progress_ratio = self.loading_progress / work
                loading_bar_width = max(1, int(progress_ratio * 720))

                loading_bar = pygame.transform.scale(loading_bar_original, (loading_bar_width, 150))
                loading_bar_rect = loading_bar.get_rect(midleft=(280, 340))

                screen.blit(loading_bg, loading_rect)
                screen.blit(loading_bar, loading_bar_rect)
            else:
                print("Chargement terminé !")
                break

            pygame.display.update()
            clock.tick(60)


