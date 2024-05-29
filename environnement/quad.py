import numpy as np
import time
import pygame


class Quad:
    def __init__(
            self,
            dimension,
    ):
        self.predateurs = []
        self.proies = []
        self.personnages = []
        self.obstacles = []
        self.dimension: np.ndarray = dimension
        self.distance_maximale = np.hypot(self.dimension[0], self.dimension[1])
        self.angle_reference = np.array([0, 1])

    def reinitialisation(self):
        for obstacle in self.obstacles:
            obstacle.reinitialisation()

    def rendu_graphique(self, fenetre):
        for obstacle in self.obstacles:
            obstacle.rendu_graphique(fenetre)

