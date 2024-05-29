import math
import numpy as np

from environnement.obstacle import Obstacle


class Personnage(Obstacle):
    def __init__(self, quad, taille, vitesse_max, acceleration):
        super().__init__(quad, taille)
        self.quad.personnages.append(self)
        self.vitesse_max = vitesse_max
        self.acceleration = acceleration
        self.en_jeu: bool = None
        self.vitesse = None

    def reinitialisation(self):
        super().reinitialisation()
        self.en_jeu = True
        self.vitesse = np.array([0, 0])

    def accelerer(self, direction):
        if np.linalg.norm(direction) > 0:
            direction = direction / np.linalg.norm(direction)

        self.vitesse = self.vitesse + direction * self.acceleration

        if self.vitesse_max == 0 or np.linalg.norm(self.vitesse) == 0:
            self.vitesse = np.array([0, 0])
        elif np.linalg.norm(self.vitesse) > self.vitesse_max:
            self.vitesse = (self.vitesse / np.linalg.norm(self.vitesse)) * self.vitesse_max

    def deplace(self, intervalle_temporel):
        nouvelle_position = self.position + self.vitesse * intervalle_temporel
        vieille_position = self.position
        self.position = nouvelle_position

        if self.controle_collision():
            self.position = vieille_position

        self.position = np.clip(self.position, a_min=[0, 0], a_max=[self.quad.dimension[0], self.quad.dimension[1]])

    def agit(self, intervalle_temporel):
        pass

    def position_obstacle_plus_proche(self):
        distance_plus_proche = math.inf
        position = None

        for obstacle in self.quad.obstacles:
            vecteur = self.position - obstacle.position
            distance = np.linalg.norm(vecteur) - obstacle.taille

            if distance_plus_proche > distance and not isinstance(obstacle, Personnage):
                distance_plus_proche = distance
                position = obstacle.position

        if position is None:
            position = np.array([-1, -1])

        return position

    def obstacle_plus_proche(self) -> Obstacle:
        distance_plus_proche = math.inf
        obstacle_plus_proche = None

        for obstacle in self.quad.obstacles:
            vecteur = self.position - obstacle.position
            distance = np.linalg.norm(vecteur) - obstacle.taille

            if distance_plus_proche > distance and not isinstance(obstacle, Personnage):
                distance_plus_proche = distance
                obstacle_plus_proche = obstacle

        return obstacle_plus_proche

    def contact_obstacle(self):
        obstacle = self.obstacle_plus_proche()
        if np.linalg.norm(self.position - obstacle.position) <= (obstacle.taille + self.taille) * 1.1:
            return True
        else:
            return False
