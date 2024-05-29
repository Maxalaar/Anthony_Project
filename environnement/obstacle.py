import numpy as np
from typing import Tuple
import pygame

from environnement.quad import Quad


class Obstacle:
    def __init__(self, quad, taille=20):
        self.quad: Quad = quad
        self.quad.obstacles.append(self)
        self.position: np.ndarray = None
        self.taille = taille
        self.couleur: Tuple[int, int, int] = (255, 255, 255)

    def reinitialisation(self):
        self.position = np.random.uniform(np.array([0, 0]), self.quad.dimension, size=2)
        mauvaise_position = self.controle_collision()

        while mauvaise_position:
            self.position = np.random.uniform(np.array([0, 0]), self.quad.dimension, size=2)
            mauvaise_position = self.controle_collision()

    def rendu_graphique(self, fenetre):
        pygame.draw.circle(fenetre, self.couleur, self.position, self.taille)

    def collision(self, autre_obstacle):
        if np.linalg.norm(self.position - autre_obstacle.position) - self.taille - autre_obstacle.taille > 0:
            return False
        else:
            return True

    def controle_collision(self):
        collision = False
        for obstacle in self.quad.obstacles:
            if obstacle.position is not None and obstacle.collision(self) and obstacle != self:
                collision = True

        for personnage in self.quad.personnages:
            if personnage.en_jeu and personnage.collision(self) and personnage != self and personnage.position is not None:
                collision = True

        return collision
