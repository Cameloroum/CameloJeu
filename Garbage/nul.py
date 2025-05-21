import pygame, sys, random

# ──────────────────── Initialisation ────────────────────
pygame.init()
largeur_fenetre, hauteur_fenetre = 800, 600
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Ghali")
clock = pygame.time.Clock()

# Sol (bande grise de 50 px tout en bas)
hauteur_sol = 50
y_sol = hauteur_fenetre - hauteur_sol          # = 550

# Foreuse
baseSize = (40, 40)
image_foreuse = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load("../vaisseau.png"), baseSize), 180
)
position_foreuse = [(largeur_fenetre - baseSize[0]) // 2, 0]
rectangle_foreuse = pygame.Rect(*position_foreuse, *baseSize)

# Laser
lasers = []                      # [x, y]
LASER_SPEED = 10
LASER_WIDTH, LASER_HEIGHT = 4, 10

# Score
score = 0
police = pygame.font.SysFont(None, 36)

# ──────────────────── Grille de blocs ────────────────────
colonnes, lignes = 20, 10

y_surface = position_foreuse[1] + baseSize[1] + 20   # ★ Mine démarre juste sous la foreuse (20 px de marge)
hauteur_zone_mine = y_sol - y_surface                # ★ Espace disponible pour la mine
largeur_bloc  = largeur_fenetre // colonnes
hauteur_bloc  = hauteur_zone_mine // lignes          # taille entière → pas de trous

points_couleurs = {                  # type : (points, couleur)
    'roche': (1,  (100, 100, 100)),
    'fer'  : (5,  (150, 150, 150)),
    'or'   : (20, (255, 215,   0))
}

grille = []
for i in range(lignes):
    rangée = []
    for j in range(colonnes):
        btype = random.choices(
            list(points_couleurs.keys()), weights=[70, 25, 5]
        )[0]
        bloc_rect = pygame.Rect(
            j * largeur_bloc,
            y_surface + i * hauteur_bloc,             # ★ Mine vers le bas
            largeur_bloc,
            hauteur_bloc
        )
        rangée.append({'type': btype, 'rect': bloc_rect})
    grille.append(rangée)

# ──────────────────── Fonctions ──────────────────────────
def dessiner():
    fenetre.fill((255, 255, 255))                     # ciel blanc

    # Blocs
    for rangée in grille:
        for bloc in rangée:
            if bloc is None:
                continue
            _, couleur = points_couleurs[bloc['type']]
            pygame.draw.rect(fenetre, couleur, bloc['rect'])

    # Sol
    pygame.draw.rect(fenetre, (100, 100, 100),
                     pygame.Rect(0, y_sol, largeur_fenetre, hauteur_sol))

    # Foreuse
    fenetre.blit(image_foreuse, position_foreuse)

    # Lasers
    for x, y in lasers:
        pygame.draw.rect(
            fenetre, (255, 0, 0),
            pygame.Rect(x - LASER_WIDTH // 2, y, LASER_WIDTH, LASER_HEIGHT)
        )

    # Score
    fenetre.blit(police.render(f"Score : {score}", True, (0, 0, 0)), (10, 10))

def deplacer_foreuse():
    touches = pygame.key.get_pressed()
    if touches[pygame.K_RIGHT] and position_foreuse[0] < largeur_fenetre - baseSize[0]:
        position_foreuse[0] += 5
    if touches[pygame.K_LEFT] and position_foreuse[0] > 0:
        position_foreuse[0] -= 5
    rectangle_foreuse.topleft = position_foreuse

def mise_a_jour_lasers():
    for laser in lasers:
        laser[1] += LASER_SPEED
    lasers[:] = [l for l in lasers if l[1] <= hauteur_fenetre]

def detecter_collision_lasers():
    global score, lasers
    lasers_restants = []
    for x, y in lasers:
        rect_laser = pygame.Rect(x - LASER_WIDTH // 2, y,
                                 LASER_WIDTH, LASER_HEIGHT)
        a_touche = False
        for i in range(lignes):
            for j in range(colonnes):
                bloc = grille[i][j]
                if bloc and rect_laser.colliderect(bloc['rect']):
                    pts, _ = points_couleurs[bloc['type']]
                    score += pts
                    grille[i][j] = None
                    a_touche = True
                    break
            if a_touche:
                break
        if not a_touche:
            lasers_restants.append([x, y])
    lasers = lasers_restants

# ──────────────────── Boucle principale ──────────────────
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            lasers.append([
                position_foreuse[0] + baseSize[0] // 2,
                position_foreuse[1] + baseSize[1]
            ])

    deplacer_foreuse()
    mise_a_jour_lasers()
    detecter_collision_lasers()
    dessiner()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
