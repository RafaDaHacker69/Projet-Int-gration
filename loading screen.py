import pygame
import sys
import threading

pygame.init()

screen = pygame.display.set_mode((1240,680))
pygame.display.set_caption("Chargement")

font = pygame.font.SysFont("Roboto",100)



clock = pygame.time.Clock()






while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()

    screen.fill("#0d0e2e")

    pygame.display.update()
    clock.tick(60)