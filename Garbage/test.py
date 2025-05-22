import pygame
import sys
import random

# Initialisation
pygame.init()
largeur_fenetre, hauteur_fenetre = 800, 600
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Ghali")
clock = pygame.time.Clock()

# Foreuse
baseSize = (40, 40)
image_foreuse = pygame.image.load("vaisseau.png")
image_foreuse = pygame.transform.scale(image_foreuse, baseSize)
image_foreuse = pygame.transform.rotate(image_foreuse, 180)
position_foreuse = [(largeur_fenetre - baseSize[0]) // 2, 0]
rectangle_foreuse = pygame.Rect(position_foreuse[0], position_foreuse[1], baseSize[0], baseSize[1])

# Energie
LARGEUR_BARRE_ENERGIE = 150
HAUTEUR_BARRE_ENERGIE = 20
X_BARRE_ENERGIE = 620
Y_BARRE_ENERGIE = 38
energie_base = 100
energie_max = 150

# Laser
lasers = []
LASER_SPEED = 10
LASER_WIDTH, LASER_HEIGHT = 4, 10

# Score
score = 0
police = pygame.font.SysFont(None, 36)

# Grille
colonnes = 20
largeur_bloc = largeur_fenetre / colonnes
hauteur_bloc = 30
SCROLL_SPEED = 1

# Blocs
points_couleurs = {
    'roche': (1, (50, 100, 100)),
    'fer': (5, (150, 150, 150)),
    'or': (20, (255, 215, 0))
}
grille = []

def generer_ligne_blocs(y):
    rangée = []
    for j in range(colonnes):
        btype = random.choices(list(points_couleurs.keys()), weights=[70, 25, 5])[0]
        bloc = pygame.Rect(j * largeur_bloc, y, largeur_bloc, hauteur_bloc)
        rangée.append({'type': btype, 'rect': bloc})
    return rangée

# Bidons
bidons = []
proba_bidon = 0.1

# Initialisation de la grille
hauteur_sol = 100
y_sol = hauteur_fenetre - hauteur_sol
for i in range(15):
    grille.append(generer_ligne_blocs(y_sol + i * hauteur_bloc))

# Dessin
def dessiner():
    fenetre.fill((255, 255, 255))

    # Sol
    pygame.draw.rect(fenetre, (100, 100, 100), pygame.Rect(0, y_sol, largeur_fenetre, hauteur_sol))

    # Blocs
    for rangée in grille:
        for bloc in rangée:
            if bloc:
                btype = bloc['type']
                _, couleur = points_couleurs[btype]
                pygame.draw.rect(fenetre, couleur, bloc['rect'])

    # Bidons
    for br in bidons:
        pygame.draw.rect(fenetre, (255, 0, 0), br)

    # Foreuse
    fenetre.blit(image_foreuse, position_foreuse)

    # Lasers
    for x, y in lasers:
        rect_laser = pygame.Rect(x - LASER_WIDTH // 2, y, LASER_WIDTH, LASER_HEIGHT)
        pygame.draw.rect(fenetre, (255, 0, 0), rect_laser)

    # Score
    texte_score = police.render(f"Score : {score}", True, (0, 0, 0))
    fenetre.blit(texte_score, (10, 10))

    # Energie
    texte_energie = police.render(f"Energy: {energie_base}/{energie_max}", True, (0, 0, 0))
    fenetre.blit(texte_energie, (X_BARRE_ENERGIE, 12))

    pygame.draw.rect(fenetre, (128, 128, 128), (X_BARRE_ENERGIE, Y_BARRE_ENERGIE, LARGEUR_BARRE_ENERGIE, HAUTEUR_BARRE_ENERGIE))
    ratio = energie_base / energie_max
    largeur_courante = int(ratio * LARGEUR_BARRE_ENERGIE)
    pygame.draw.rect(fenetre, (0, 255, 0), (X_BARRE_ENERGIE, Y_BARRE_ENERGIE, largeur_courante, HAUTEUR_BARRE_ENERGIE))

# Déplacement foreuse
def deplacer_foreuse():
    touches = pygame.key.get_pressed()
    if touches[pygame.K_RIGHT] and position_foreuse[0] < largeur_fenetre - baseSize[0]:
        position_foreuse[0] += 5
    if touches[pygame.K_LEFT] and position_foreuse[0] > 0:
        position_foreuse[0] -= 5
    rectangle_foreuse.topleft = position_foreuse

# Mise à jour laser
def mise_a_jour_lasers():
    for laser in lasers:
        laser[1] += LASER_SPEED
    lasers[:] = [l for l in lasers if l[1] <= hauteur_fenetre]

# Collision laser
def detecter_collision_lasers():
    global score, lasers
    nouveaux_lasers = []
    for x, y in lasers:
        rect_laser = pygame.Rect(x - LASER_WIDTH // 2, y, LASER_WIDTH, LASER_HEIGHT)
        collision = False
        for i in range(len(grille)):
            for j in range(len(grille[i])):
                bloc = grille[i][j]
                if bloc and rect_laser.colliderect(bloc['rect']):
                    pts, _ = points_couleurs[bloc['type']]
                    score += pts
                    if random.random() < proba_bidon:
                        bidons.append(bloc['rect'].copy())
                    grille[i][j] = None
                    collision = True
                    break
            if collision:
                break
        if not collision:
            nouveaux_lasers.append([x, y])
    lasers = nouveaux_lasers

# Collision bidons
def detecter_collision_bidons():
    global energie_base
    for bidon in bidons[:]:
        if rectangle_foreuse.colliderect(bidon):
            energie_base = min(energie_max, energie_base + 30)
            bidons.remove(bidon)

# Scroll
def scroll_vers_haut():
    for ligne in grille:
        for bloc in ligne:
            if bloc:
                bloc['rect'].y -= SCROLL_SPEED
    for i in range(len(bidons)):
        bidons[i].y -= SCROLL_SPEED
    if grille and grille[0][0]['rect'].y + hauteur_bloc < 0:
        grille.pop(0)
    y_nouvelle_ligne = grille[-1][0]['rect'].y + hauteur_bloc
    grille.append(generer_ligne_blocs(y_nouvelle_ligne))

# Boucle principale
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and energie_base > 0:
            depart_x = position_foreuse[0] + baseSize[0] // 2
            depart_y = position_foreuse[1] + baseSize[1]
            lasers.append([depart_x, depart_y])
            energie_base -= 1

    deplacer_foreuse()
    mise_a_jour_lasers()
    detecter_collision_lasers()
    detecter_collision_bidons()
    scroll_vers_haut()
    dessiner()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
