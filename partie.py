import numpy as np
import time
import pygame

from environnement.quad import Quad
from environnement.proie import Proie
from environnement.predateur import Predateur
from environnement.obstacle import Obstacle
from environnement.jeu import Jeu


def partie(
        nombre_manches=1,
        dimension=np.array([500, 500]),
        nombre_obstacles=2,
        tailles_obstacles=40,
        nombre_proies=1,
        taille_proies=10,
        vitesse_maximale_proies=15,
        acceleration_proies=2,
        nombre_predateurs=1,
        taille_predateurs=10,
        vitesse_maximale_predateurs=15,
        acceleration_predateurs=2,
        temps_jeu_maximum=200,
        intervalle_temporel=0.01,
        rendre_graphiquement=False,
        fps=30,
):
    quad = Quad(dimension)
    proies = []
    predateurs = []
    obstacles = []

    for i in range(nombre_obstacles):
        obstacles.append(
            Obstacle(
                quad,
                tailles_obstacles
            )
        )

    for i in range(nombre_proies):
        proies.append(
            Proie(
                quad,
                taille_proies,
                vitesse_maximale_proies,
                acceleration_proies,
            )
        )

    for i in range(nombre_predateurs):
        predateurs.append(
            Predateur(
                quad,
                taille_predateurs,
                vitesse_maximale_predateurs,
                acceleration_predateurs,
            )
        )

    jeu = Jeu(
        quad,
        predateurs,
        proies,
        temps_jeu_maximum,
        intervalle_temporel,
        rendre_graphiquement,
        fps,
    )
    score = 0
    manche_courante = 0
    while manche_courante < nombre_manches:
        jeu.increment()

        if jeu.verification_victoire_proies():
            score += 1
            manche_courante += 1
            jeu.reinitialisation()
        if jeu.verification_victoire_perdateurs():
            manche_courante += 1
            jeu.reinitialisation()

    return score/manche_courante
