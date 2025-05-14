import pygame
import sys
import random

# Initialisation
pygame.init()
largeur_fenetre, hauteur_fenetre = 800, 600
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Ghali")
clock = pygame.time.Clock()

# Paramètres du sol
hauteur_sol = 50
y_sol = hauteur_fenetre - hauteur_sol

# Foreuse
baseSize = (40, 40)
image_foreuse = pygame.image.load("vaisseau.png")
image_foreuse = pygame.transform.scale(image_foreuse, baseSize)
image_foreuse = pygame.transform.rotate(image_foreuse, 180)
position_foreuse = [(largeur_fenetre - baseSize[0]) // 2, 0]
rectangle_foreuse = pygame.Rect(position_foreuse[0], position_foreuse[1], baseSize[0], baseSize[1])

# Laser
lasers = []
LASER_SPEED = 10
LASER_WIDTH, LASER_HEIGHT = 4, 10

# Score
score = 0
police = pygame.font.SysFont(None, 36)

# 1. Grille de blocs (20×10) sous le sol
colonnes, lignes = 20, 10
largeur_bloc = largeur_fenetre / colonnes
hauteur_bloc = (hauteur_fenetre - y_sol) / lignes
# Types de blocs et leurs points + couleurs
points_couleurs = {
    'roche': (1,   (100, 100, 100)),
    'fer':   (5,   (150, 150, 150)),
    'or':    (20,  (255, 215,   0))
}
# Création de la grille
grille = []
for i in range(lignes):
    rangée = []
    for j in range(colonnes):
        btype = random.choices( list(points_couleurs.keys()), weights=[70, 25, 5])[0]  #bloc type
        bloc = pygame.Rect(
            j * largeur_bloc,  # pos x
            y_sol + i * hauteur_bloc,  #pos y
            largeur_bloc, #largeur
            hauteur_bloc # hauteur
        )
        rangée.append({'type': btype, 'rect': bloc})
    grille.append(rangée)

def dessiner():
    fenetre.fill((255, 255, 255))
    # Sol
    pygame.draw.rect(
        fenetre,
        (100, 100, 100),
        pygame.Rect(0, y_sol, largeur_fenetre, hauteur_sol)
    )
    # Blocs
    for rangée in grille:
        for bloc in rangée:
            if bloc is None:
                continue
            btype = bloc['type']
            _, couleur = points_couleurs[btype]
            pygame.draw.rect(fenetre, couleur, bloc['rect'])
    # Foreuse
    fenetre.blit(image_foreuse, position_foreuse)
    # Lasers
    for x, y in lasers:
        rect_laser = pygame.Rect(x - LASER_WIDTH//2, y, LASER_WIDTH, LASER_HEIGHT)
        pygame.draw.rect(fenetre, (255, 0, 0), rect_laser)
    # Score
    texte_score = police.render(f"Score : {score}", True, (0, 0, 0))
    fenetre.blit(texte_score, (10, 10))

def deplacer_foreuse():
    touches = pygame.key.get_pressed()
    if touches[pygame.K_RIGHT] and position_foreuse[0] < largeur_fenetre - baseSize[0]:
        position_foreuse[0] += 5
    if touches[pygame.K_LEFT] and position_foreuse[0] > 0:
        position_foreuse[0] -= 5
    rectangle_foreuse.topleft = position_foreuse

def mise_a_jour_lasers():


    # déplacer les lasers
    for laser in lasers:
        laser[1] += LASER_SPEED
    # supprimer hors écran
    temp = []
    for l in lasers:
        if 0 <= l[1] <= hauteur_fenetre:
            temp.append(l)
    lasers[:] = temp

def detecter_collision_lasers():
    global score, lasers
    nouveaux_lasers = []
    # Pour chaque laser
    for x, y in lasers:
        rect_laser = pygame.Rect(
            x - LASER_WIDTH // 2,
            y,
            LASER_WIDTH,
            LASER_HEIGHT
        )
        collision = False
        # Parcours de la grille
        for i in range(len(grille)):
            for j in range(len(grille[i])):
                bloc = grille[i][j]
                if bloc is not None and rect_laser.colliderect(bloc['rect']):
                    pts, _ = points_couleurs[bloc['type']]
                    score += pts
                    grille[i][j] = None   # suppression du bloc
                    collision = True

            if collision:
                break
        # Si pas de collision, on garde le laser pour la suite
        if not collision:
            nouveaux_lasers.append([x, y])
    lasers = nouveaux_lasers



# Boucle principale
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # création d'un laser sous la foreuse
            depart_x = position_foreuse[0] + baseSize[0] // 2
            depart_y = position_foreuse[1] + baseSize[1]
            lasers.append([depart_x, depart_y])


    deplacer_foreuse()
    mise_a_jour_lasers()
    detecter_collision_lasers()
    dessiner()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
