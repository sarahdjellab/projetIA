import numpy as np
import random
import os
import heapq

# Fonction pour afficher proprement la grille
def afficher_grille(grille):
    for ligne in grille:
        print("|", end=" ")
        for case in ligne:
            print(f"{case:3}", end=" ")
        print("|")

# Fonction pour générer les obstacles selon le niveau
def generer_obstacles(grille, pourcentage):
    nb_lignes = len(grille)
    nb_colonnes = len(grille[0])
    nb_cases = nb_lignes * nb_colonnes
    nb_obstacles = int(nb_cases * pourcentage)

    obstacles = set()
    while len(obstacles) < nb_obstacles:
        i = random.randint(0, nb_lignes - 1)
        j = random.randint(0, nb_colonnes - 1)
        if grille[i][j] == ".":
            grille[i][j] = "#"
            obstacles.add((i, j))
    return obstacles

# Demande à l'utilisateur la taille de la grille
def demander_taille():
    while True:
        try:
            lignes = int(input("Entrez le nombre de lignes (> 2) : "))
            colonnes = int(input("Entrez le nombre de colonnes (> 2) : "))
            if lignes > 2 and colonnes > 2:
                return lignes, colonnes
            else:
                print("La taille doit être supérieure à 2.")
        except ValueError:
            print("Veuillez entrer des entiers valides.")

# Demande à l'utilisateur le niveau de difficulté
def demander_difficulte():
    print("\nChoisissez le niveau de difficulté :")
    print("1. Facile ")
    print("2. Moyen ")
    print("3. Difficile ")
    while True:
        choix = input("Votre choix (1/2/3) : ")
        if choix == "1":
            return 0.10
        elif choix == "2":
            return 0.30
        elif choix == "3":
            return 0.50
        else:
            print("Choix invalide. Veuillez entrer 1, 2 ou 3.")

# Choisit un point vide au hasard sur la grille
def choisir_point(grille):
    lignes, colonnes = len(grille), len(grille[0])
    while True:
        i, j = random.randint(0, lignes - 1), random.randint(0, colonnes - 1)
        if grille[i][j] == ".":
            return (i, j)

# Heuristique de Manhattan
def heuristique(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* algorithm
def astar(grille, start, goal):
    voisins = [(0,1), (1,0), (0,-1), (-1,0)]
    open_set = []
    heapq.heappush(open_set, (0 + heuristique(start, goal), 0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, cost, current = heapq.heappop(open_set)

        if current == goal:
            chemin = []
            while current in came_from:
                chemin.append(current)
                current = came_from[current]
            chemin.reverse()
            return chemin

        for dx, dy in voisins:
            voisin = (current[0] + dx, current[1] + dy)
            if 0 <= voisin[0] < len(grille) and 0 <= voisin[1] < len(grille[0]):
                if grille[voisin[0]][voisin[1]] == "#":
                    continue
                tentative_g = g_score[current] + 1
                if voisin not in g_score or tentative_g < g_score[voisin]:
                    g_score[voisin] = tentative_g
                    f_score = tentative_g + heuristique(voisin, goal)
                    heapq.heappush(open_set, (f_score, tentative_g, voisin))
                    came_from[voisin] = current

    return None  # Pas de chemin trouvé

# Initialisation principale
def initialiser_grille():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Agent Intelligent A* ===")
    lignes, colonnes = demander_taille()
    difficulte = demander_difficulte()

    grille = [["." for _ in range(colonnes)] for _ in range(lignes)]

    obstacles = generer_obstacles(grille, difficulte)

    point_depart = choisir_point(grille)
    grille[point_depart[0]][point_depart[1]] = "S"

    point_arrivee = choisir_point(grille)
    while point_arrivee == point_depart:
        point_arrivee = choisir_point(grille)
    grille[point_arrivee[0]][point_arrivee[1]] = "G"

    print("\nVoici la grille initialisée :\n")
    afficher_grille(grille)

    return grille, point_depart, point_arrivee

if __name__ == "__main__":
    grille, depart, arrivee = initialiser_grille()
    chemin = astar(grille, depart, arrivee)

    if chemin:
        for x, y in chemin:
            if grille[x][y] == ".":
                grille[x][y] = "*"
        print("\nChemin trouvé :\n")
    else:
        print("\nAucun chemin trouvé entre S et G.\n")

    afficher_grille(grille)
