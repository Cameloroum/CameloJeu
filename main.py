import pygame
import sys
import random

# Initialisation
pygame.init()
largeur_fenetre, hauteur_fenetre = 800, 600
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
image_fond = pygame.image.load("minebackground.png")
image_fond = pygame.transform.scale(image_fond, (largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Ghali")
clock = pygame.time.Clock()

# Foreuse
baseSize = (20, 20)
image_foreuse = pygame.image.load("vaisseau.png")
image_foreuse = pygame.transform.scale(image_foreuse, baseSize)
image_base = image_foreuse
position_foreuse = [(largeur_fenetre - baseSize[0]) // 2, 0]
rectangle_foreuse = pygame.Rect(position_foreuse[0], position_foreuse[1], baseSize[0], baseSize[1])

# Energie
LARGEUR_BARRE_ENERGIE = 150
HAUTEUR_BARRE_ENERGIE = 20
X_BARRE_ENERGIE = 620
Y_BARRE_ENERGIE = 38
energie_base = 100
energie_max = 150

# Forage
forage = False
last_forage = 0
bloc_en_forage = None
forage_cooldown_base = 750
forage_cooldown_bonus = 0
direction_foreuse = "droite"  # ou "gauche" ou "bas"
vitesse_foreuse = 2
animation_offset = 0
animation_direction = 1
anim_en_cours = False

# Score
score = 0
police = pygame.font.SysFont(None, 36)

# Bidons et objets
vies = 3
bidons = []
proba_bidon = 0.1
bombes = []
vitesse_bombe = 4
proba_bombe = 0.01
temps_bombe = 3000
tremblement_duree = 0
flash_duree = 0

# Boutique
boutique_active = False
vitesse_bonus = 1.0
energie_max_bonus = 0
vies_bonus = 0
message_achat = ""
message_achat_time = 0
# Grille
colonnes = 20
largeur_bloc = largeur_fenetre / colonnes
hauteur_bloc = 30
SCROLL_SPEED = 2
profondeur = 0
# Blocs
points_couleurs = {
    'roche': (1, (50, 100, 100)),
    'fer': (5, (150, 150, 150)),
    'or': (20, (255, 215, 0))
}
grille = []


def generer_ligne_blocs(y):
    global proba_bombe
    rangée = []
    for j in range(colonnes):
        btype = random.choices(list(points_couleurs.keys()), weights=[70, 25, 5])[0]  # chance d'apparition
        bloc = pygame.Rect(j * largeur_bloc, y, largeur_bloc, hauteur_bloc)
        proba_bombe = 0.01 + 0.015 * (profondeur // 1000)
        instable = random.random() < proba_bombe  # % de chance d’être instable
        rangée.append({'type': btype, 'rect': bloc, 'instable': instable})
    return rangée


# Initialisation de la grille
hauteur_sol = 100
y_sol = hauteur_fenetre - hauteur_sol
for i in range(15):
    grille.append(generer_ligne_blocs(y_sol + i * hauteur_bloc))


# Dessin
def dessiner():
    global tremblement_duree, flash_duree, message_achat_time, message_achat

    # Appliquer un léger décalage si tremblement actif
    if tremblement_duree > 0:
        offset_x = random.randint(-5, 5)  #  bouge aleatoirement gauche droite
        offset_y = random.randint(-5, 5)
        tremblement_duree -= 1
    else:
        offset_x = 0
        offset_y = 0

    # Surface intermédiaire pour l’effet de décalage
    surface_temp = pygame.Surface((largeur_fenetre, hauteur_fenetre))
    surface_temp.blit(image_fond, (0,0))

    # Sol
    pygame.draw.rect(surface_temp, (100, 100, 100), pygame.Rect(0, y_sol, largeur_fenetre, hauteur_sol))

    # Blocs
    for rangée in grille:
        for bloc in rangée:
            if bloc:
                btype = bloc['type']
                _, couleur = points_couleurs[btype]
                pygame.draw.rect(surface_temp, couleur, bloc['rect'])

    # Bidons
    for br in bidons:
        pygame.draw.rect(surface_temp, (0, 230, 0), br)

    # Bombes
    temps_actuel = pygame.time.get_ticks()
    for bombe in bombes:
        temps_ecoule = temps_actuel - bombe['debut']
        if (temps_ecoule // 300) % 2 == 0:
            pygame.draw.circle(surface_temp, (255, 0, 0), bombe['rect'].center, 6)

    texte_prob = police.render(f"Proba bombes: {round(proba_bombe * 100, 2)}%", True, (150, 0, 0))
    surface_temp.blit(texte_prob, (10, 70))

    # Foreuse
    pos_anim = position_foreuse.copy()
    if anim_en_cours:
        pos_anim[1] += animation_offset
    surface_temp.blit(image_foreuse, pos_anim)

    # Score
    texte_score = police.render(f"Score : {score}", True, (0, 0, 0))
    surface_temp.blit(texte_score, (10, 10))

    # Energie
    texte_energie = police.render(f"Energy: {energie_base}/{energie_max + energie_max_bonus}", True, (0, 0, 0))
    surface_temp.blit(texte_energie, (X_BARRE_ENERGIE, 12))
    pygame.draw.rect(surface_temp, (128, 128, 128),
                     (X_BARRE_ENERGIE, Y_BARRE_ENERGIE, LARGEUR_BARRE_ENERGIE, HAUTEUR_BARRE_ENERGIE))
    ratio = energie_base / (energie_max + energie_max_bonus)
    largeur_courante = int(ratio * LARGEUR_BARRE_ENERGIE)
    pygame.draw.rect(surface_temp, (0, 255, 0),
                     (X_BARRE_ENERGIE, Y_BARRE_ENERGIE, largeur_courante, HAUTEUR_BARRE_ENERGIE))

    # Profondeur
    texte_profondeur = police.render(f"Profondeur: {profondeur}", True, (0, 0, 0))
    surface_temp.blit(texte_profondeur, (10, 30))

    # Vies
    texte_vies = police.render(f"Vies: {vies}", True, (0, 0, 0))
    surface_temp.blit(texte_vies, (10, 50))

    # Appliquer le tremblement en affichant la surface avec décalage
    fenetre.blit(surface_temp, (offset_x, offset_y))

    # Flash
    if flash_duree > 0:  # faire gaffe à laisser ça en dernier (avant la boutique quand même)
        flash = pygame.Surface((largeur_fenetre, hauteur_fenetre))
        flash.set_alpha(100)  # Gestion de la transparence (0 = transparent, 255 = opaque)
        flash.fill((255, 255, 0))
        fenetre.blit((flash), (0, 0))
        flash_duree -= 1

    # Boutique
    if boutique_active:
        afficher_boutique()

    if message_achat:
        if pygame.time.get_ticks() - message_achat_time < 3000:   # le message reste affiché 3s
            confirmation = police.render(message_achat, True, (0, 0, 0))
            rect_msg = confirmation.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre - 40))
            fenetre.blit(confirmation, rect_msg)
        else:
            message_achat = ""  # on l'efface ensuite


def afficher_game_over():
    grande_police = pygame.font.SysFont(None, 100)
    texte = grande_police.render("GAME OVER", True, (255, 0, 0))
    rect_texte = texte.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2))
    fenetre.blit(texte, rect_texte)
    pygame.display.flip()
    pygame.time.wait(3000)


def afficher_boutique():
    surface_boutique = pygame.Surface((400, 200))
    surface_boutique.fill((220, 220, 220))
    pygame.draw.rect(surface_boutique, (0, 0, 0), surface_boutique.get_rect(), 2)

    titre = police.render("Boutique", True, (0, 0, 0))
    opt1 = police.render("1 - Foreuse+ (100 pts)", True, (0, 0, 0))
    opt2 = police.render("2 - Réservoir+ (150 pts)", True, (0, 0, 0))
    opt3 = police.render("3 - Blindage+ (200 pts)", True, (0, 0, 0))

    surface_boutique.blit(titre, (150, 10))
    surface_boutique.blit(opt1, (20, 60))
    surface_boutique.blit(opt2, (20, 100))
    surface_boutique.blit(opt3, (20, 140))

    # Centrer la boutique sur l'écran
    rect = surface_boutique.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2))
    fenetre.blit(surface_boutique, rect.topleft)


# Déplacement foreuse
def deplacer_foreuse():
    global direction_foreuse
    if forage:
        return
    touches = pygame.key.get_pressed()

    # Droite
    if touches[pygame.K_RIGHT] and position_foreuse[0] < largeur_fenetre - baseSize[0]:
        future_rect = rectangle_foreuse.move(5, 0)
        bloque = False
        for ligne in grille:
            for bloc in ligne:
                if bloc and future_rect.colliderect(bloc['rect']):
                    bloque = True
                    break
            if bloque:
                break
        if not bloque:
            direction_foreuse = "droite"
            position_foreuse[0] += int(5 * vitesse_bonus)

    # Gauche
    if touches[pygame.K_LEFT] and position_foreuse[0] > 0:
        future_rect = rectangle_foreuse.move(-5, 0)
        bloque = False
        for ligne in grille:
            for bloc in ligne:
                if bloc and future_rect.colliderect(bloc['rect']):
                    bloque = True
                    break
            if bloque:
                break
        if not bloque:
            direction_foreuse = "gauche"
            position_foreuse[0] -= int(5 * vitesse_bonus)

    # Bas (juste pour orientation)
    if touches[pygame.K_DOWN]:
        direction_foreuse = "bas"

    rectangle_foreuse.topleft = position_foreuse


def mettre_a_jour_image_foreuse():
    global image_foreuse
    if direction_foreuse == "bas":
        image_foreuse = pygame.transform.rotate(image_base, 180)
    elif direction_foreuse == "gauche":
        image_foreuse = pygame.transform.rotate(image_base, 90)
    elif direction_foreuse == "droite":
        image_foreuse = pygame.transform.rotate(image_base, -90)


def gerer_forage():
    global forage, last_forage, bloc_en_forage, score, energie_base, anim_en_cours, bombes

    temps_actuel = pygame.time.get_ticks()

    if forage:
        if temps_actuel - last_forage >= forage_cooldown_base - forage_cooldown_bonus :
            if bloc_en_forage:
                pts, _ = points_couleurs[bloc_en_forage['type']]
                score += pts
                energie_base -= 1
                if bloc_en_forage['instable']:
                    bombes.append({
                        'rect': bloc_en_forage['rect'].copy(),
                        'debut': pygame.time.get_ticks()
                    })
                if random.random() < proba_bidon and bloc_en_forage['instable'] == False:   # un bidon ne doit pas apparaitre sur un bloc instable
                    bidons.append(bloc_en_forage['rect'].copy())
                for ligne in grille:
                    if bloc_en_forage in ligne:
                        ligne.remove(bloc_en_forage)
                        break

            forage = False
            bloc_en_forage = None
    else:
        for ligne in grille:
            for bloc in ligne:
                if not bloc:
                    continue
                rect = bloc['rect']
                if direction_foreuse == "bas":
                    cible = pygame.Rect(rectangle_foreuse.centerx - largeur_bloc // 2, rectangle_foreuse.bottom,
                                        largeur_bloc, 1)
                elif direction_foreuse == "gauche":
                    cible = pygame.Rect(rectangle_foreuse.left - 1, rectangle_foreuse.centery, 1, hauteur_bloc)
                elif direction_foreuse == "droite":
                    cible = pygame.Rect(rectangle_foreuse.right, rectangle_foreuse.centery, 1, hauteur_bloc)
                else:
                    continue

                if cible.colliderect(rect):
                    forage = True
                    last_forage = temps_actuel
                    bloc_en_forage = bloc
                    anim_en_cours = True
                    return  # On fore un seul bloc


def gerer_bombes():
    global vies, continuer, tremblement_duree, flash_duree
    temps_actuel = pygame.time.get_ticks()
    for bombe in bombes[:]:
        if temps_actuel - bombe['debut'] >= temps_bombe:
            if rectangle_foreuse.colliderect(bombe['rect']):
                vies -= 1
                tremblement_duree = 20
                flash_duree = 8
                if vies <= 0:
                    afficher_game_over()
                    continuer = False  # ON ARRETE LE JEU
            bombes.remove(bombe)

# Collision bidons
def detecter_collision_bidons():
    global energie_base
    for bidon in bidons[:]:
        if rectangle_foreuse.colliderect(bidon):
            energie_base = min(energie_max, energie_base + 30)
            bidons.remove(bidon)


# Scroll
def scroll_vers_haut():
    global profondeur
    if forage:
        return

    if direction_foreuse == "bas":   # le vaisseau ne se déplace que par illusion
        for ligne in grille:
            for bloc in ligne:
                if bloc and rectangle_foreuse.colliderect(bloc['rect']):
                    gerer_forage()
                    return

        for ligne in grille:
            for bloc in ligne:
                if bloc:
                    bloc['rect'].y -= SCROLL_SPEED

        for i in range(len(bidons)):
            bidons[i].y -= SCROLL_SPEED

        for i in range(len(bombes)):
            bombes[i]['rect'].y -= SCROLL_SPEED

        if grille and grille[0][0]['rect'].y + hauteur_bloc < 0:
            grille.pop(0)

        y_nouvelle_ligne = grille[-1][0]['rect'].y + hauteur_bloc
        grille.append(generer_ligne_blocs(y_nouvelle_ligne))
        profondeur += 1


def gerer_boutique_evenements(event):
    global boutique_active, vitesse_bonus, forage_cooldown_bonus, energie_max_bonus, vies_bonus, score, vies, message_achat, message_achat_time

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_b:
            boutique_active = not boutique_active

        if boutique_active:
            if event.key == pygame.K_1 and score >= 100:
                vitesse_bonus = 1.5
                forage_cooldown_bonus += 100
                score -= 100
                message_achat = "Foreuse améliorée ! "
                message_achat_time = pygame.time.get_ticks()
            elif event.key == pygame.K_2 and score >= 150:
                energie_max_bonus = 50  # passe de 150 à 200
                score -= 150
                message_achat = "Réservoir amélioré !"
                message_achat_time = pygame.time.get_ticks()

            elif event.key == pygame.K_3 and score >= 200:
                vies += 1
                vies_bonus += 1
                score -= 200
                message_achat = "Blindage amélioré !"
                message_achat_time = pygame.time.get_ticks()


# Boucle principale
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        gerer_boutique_evenements(event)    # je check en permanence si la boutique est ouverte pour pouvoir avoir la condition de pause

    if not boutique_active:    # Mon code se met en pause si la boutique est ouverte
        energie_base -= 0.01
        deplacer_foreuse()
        mettre_a_jour_image_foreuse()
        detecter_collision_bidons()
        gerer_forage()
        scroll_vers_haut()
        if forage and anim_en_cours:
            animation_offset += animation_direction
            if abs(animation_offset) >= 2:  # modifier cette valeur pour que le vaisseau bouge davantage
                animation_direction *= -1
            if animation_offset == 0 and animation_direction == -1:
                anim_en_cours = False  # Fin de l'animation
        else:
            animation_offset = 0
            animation_direction = 1

        gerer_bombes()

    dessiner()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
