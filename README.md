| Fonction                           | Rôle                                                                                                          |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `generer_ligne_blocs(y)`           | Génère une ligne de blocs (roche, fer, or) à une position verticale donnée.                                   |
| `dessiner()`                       | Affiche tous les éléments du jeu : fond, blocs, foreuse, score, énergie, etc.                                 |
| `afficher_game_over()`             | Affiche l'écran de fin "GAME OVER" pendant 3 secondes.                                                        |
| `afficher_boutique()`              | Affiche le menu de boutique permettant d’acheter des améliorations.                                           |
| `deplacer_foreuse()`               | Gère le déplacement gauche/droite de la foreuse et l’orientation vers le bas.                                 |
| `mettre_a_jour_image_foreuse()`    | Met à jour l’image du vaisseau en fonction de sa direction.                                                   |
| `gerer_forage()`                   | Lance un forage si un bloc est détecté devant la foreuse, applique ses effets (score, énergie, bombe, bidon). |
| `gerer_bombes()`                   | Gère les explosions de bombes et applique les effets de dégâts (flash, vies, tremblement).                    |
| `detecter_collision_bidons()`      | Recharge l’énergie si la foreuse entre en contact avec un bidon vert.                                         |
| `scroll_vers_haut()`               | Fait défiler les blocs vers le haut pour simuler la descente du vaisseau.                                     |
| `gerer_boutique_evenements(event)` | Gère les interactions avec la boutique via le clavier (touches `B`, `1`, `2`, `3`).                           |
