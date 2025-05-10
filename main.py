import pygame
import random
import sys

# Initialisation
pygame.init()
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Ghali")
clock = pygame.time.Clock()
police = pygame.font.SysFont(None, 36)

baseSize = (40,40)
imageVaisseau = pygame.image.load("ship.png")  # trouver des sprites pour faire acte de foreuse
imageVaisseau = pygame.transform.scale(imageVaisseau, (baseSize))
positionVaisseau = (300,525)

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

def dessiner():

    fenetre.blit(imageVaisseau, positionVaisseau)
# Boucle principale
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

    dessiner()



    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()
