import pygame
import sys

# Initialisation
pygame.init()
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Ghali")
clock = pygame.time.Clock()

# Chargement du vaisseau foreur
baseSize = (40, 40)
imageVaisseau = pygame.image.load("vaisseau.png")  # remplacer par votre sprite de foreuse
imageVaisseau = pygame.transform.scale(imageVaisseau, baseSize)

# Calcul de la position pour centrer le vaisseau en haut
x_vaisseau = (largeur - baseSize[0]) // 2
y_vaisseau = 0  # tout en haut
positionVaisseau = (x_vaisseau, y_vaisseau)

# Couleurs
BLANC = (255, 255, 255)
GRIS = (100, 100, 100)

# Hauteur du sol
hauteur_sol = 50

def dessiner():
    fenetre.fill(BLANC)  # fond blanc

    # Dessiner le sol gris en bas
    pygame.draw.rect(
        fenetre,
        GRIS,
        pygame.Rect(0, hauteur - hauteur_sol, largeur, hauteur_sol)
    )

    # Afficher le vaisseau foreur centré en haut
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
