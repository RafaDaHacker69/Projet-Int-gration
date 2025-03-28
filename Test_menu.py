import pygame

class Menu:
    def __init__(self,screen):
        self.screen = screen


    def show_menu(self):
        menu_running = True
        while menu_running:
            self.screen.fill((255, 255, 255))  # Fond blanc
            font = pygame.font.Font(None, 60)
            text = font.render("Contrôle!", True, (0, 0, 0))
            button_font = pygame.font.Font(None, 50)
            button_text = button_font.render("Jouer", True, (255, 255, 255))

            button_rect = pygame.Rect(520, 300, 200, 80)  # Rectangle du bouton

            pygame.draw.rect(self.screen, (0, 120, 250), button_rect)  # Bouton bleu
            self.screen.blit(text, (520, 150))
            self.screen.blit(button_text, (580, 320))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        menu_running = False