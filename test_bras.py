
from Bras_Rotatif import Bras_Rotatif
import pygame.event

# Initialisation de pygame
pygame.init()

# Définir la taille de la fenêtre (pour capturer les événements)
screen = pygame.display.set_mode((400, 300))

posx = 100
posy = 100

bras_rotatif = Bras_Rotatif(0,0.01,0,0)

rectjoueur = pygame.Surface((20,75))
rectjoueur.fill((255,255,255))
rect = pygame.Surface((100,80),pygame.SRCALPHA)
#rect.fill("green")
background = pygame.Surface((400,300))
background.fill("black")
pygame.draw.rect(rect,(255,0,0),(45,30,40,20))
screen.blit(background,(0,0))
screen.blit(rect,(posx,posy))



i=0
t=0
omega=0
rec_taille=rect.get_rect()
rec_centre_x=rec_taille.center[0]
rec_centre_y=rec_taille.center[1]



running = True
while running:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        screen.blit(rectjoueur,(posx-0.1,posy))
        posx=posx-0.1
    if keys[pygame.K_d]:
        screen.blit(rectjoueur,(posx+0.1,posy))
        posx=posx+0.1
    if keys[pygame.K_LSHIFT]:

        t+=0.001
        i-=bras_rotatif.Calcul_de_vitesse_angulaire(omega,t,bras_rotatif.alpha,bras_rotatif.theta)


    rect_rotated = pygame.transform.rotate(rect, i)
    rectangle_rot_taille = rect_rotated.get_rect()
    rectangle_rot_centre_x = rectangle_rot_taille.center[0]
    rectangle_rot_centre_y = rectangle_rot_taille.center[1]
    diff_x = rectangle_rot_centre_x - rec_centre_x
    diff_y = rectangle_rot_centre_y - rec_centre_y
    screen.blit(background,(0,0))
    screen.blit(rectjoueur,(posx+30,posy+20))
    screen.blit(rect_rotated,(posx-diff_x, posy-diff_y))
    #i-=0.01
    #pygame.time.delay(100)

    # Gère les événements (quitter ou appui sur le bouton)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Arrête la boucle si la fenêtre est fermée
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                t = 0



    pygame.display.update()  # Met à jour l'écran

pygame.quit()
