import math
import numpy as np

from environnement.personnage import Personnage


class Proie(Personnage):
    def __init__(self, quad, taille, vitesse_max, acceleration):
        super().__init__(quad, taille, vitesse_max, acceleration)
        self.couleur = (0, 255, 0)
        self.quad.proies.append(self)

    def agit(self, intervalle_temporel):
        self.accelerer(self.direction_fuite())
        self.deplace(intervalle_temporel)

    def direction_fuite(self):
        distance_plus_proche = math.inf
        direction = np.array([0, 0])

        for predateur in self.quad.predateurs:
            vecteur = self.position - predateur.position
            distance = np.linalg.norm(vecteur) - predateur.taille

            if distance_plus_proche > distance:
                distance_plus_proche = distance
                direction = vecteur / distance

        for obstacle in self.quad.obstacles:
            vecteur = self.position - obstacle.position
            distance = np.linalg.norm(vecteur) - obstacle.taille

            if distance_plus_proche > distance and obstacle != self:
                distance_plus_proche = distance
                direction = vecteur / distance

        bords = []
        bords.append((0, self.position[1]))
        bords.append((self.quad.dimension[0], self.position[1]))
        bords.append((self.position[0], 0))
        bords.append((self.position[0], self.quad.dimension[1]))

        for bord in bords:
            vecteur = self.position - bord
            distance = np.linalg.norm(vecteur)

            if distance_plus_proche > distance:
                distance_plus_proche = distance
                if distance > 0:
                    direction = vecteur / distance

        direction / np.linalg.norm(direction)
        return direction

    def position_predateur_plus_proche(self):
        distance_plus_proche = math.inf
        position = None

        for predateur in self.quad.predateurs:
            vecteur = self.position - predateur.position
            distance = np.linalg.norm(vecteur) - predateur.taille

            if distance_plus_proche > distance and predateur.en_jeu:
                distance_plus_proche = distance
                position = predateur.position

        if position is None:
            position = np.array([-1, -1])

        return position

    def observation(self):
        # position_predateur = self.position_predateur_plus_proche() - self.position
        # position_obstacle = self.position_obstacle_plus_proche() - self.position
        # position_soi = self.position
        # return np.concatenate([position_predateur, position_obstacle, position_soi]) / self.quad.distance_maximale

        # vecteur_predateur = self.position_predateur_plus_proche() - self.position
        # distance_predateur = np.linalg.norm(vecteur_predateur) / self.quad.distance_maximale
        # angle_predateur = np.arctan2(vecteur_predateur[0], vecteur_predateur[1]) / np.pi
        #
        # vecteur_obstacle = self.position_obstacle_plus_proche() - self.position
        # distance_obstacle = np.linalg.norm(vecteur_obstacle) / self.quad.distance_maximale
        # angle_obstacle = np.arctan2(vecteur_obstacle[0], vecteur_obstacle[1]) / np.pi
        #
        # position_soi = self.position / self.quad.distance_maximale
        #
        # return np.concatenate([np.array([distance_predateur, angle_predateur, distance_obstacle, angle_obstacle]), position_soi])

        vecteur_predateur = self.position_predateur_plus_proche() - self.position
        distance_predateur = np.linalg.norm(vecteur_predateur) / self.quad.distance_maximale
        angle_predateur = np.arctan2(vecteur_predateur[0], vecteur_predateur[1]) / np.pi

        vecteur_obstacle = self.position_obstacle_plus_proche() - self.position
        distance_obstacle = np.linalg.norm(vecteur_obstacle) / self.quad.distance_maximale
        angle_obstacle = np.arctan2(vecteur_obstacle[0], vecteur_obstacle[1]) / np.pi

        angle_vitesse = np.arctan2(self.vitesse[0], self.vitesse[1]) / np.pi

        # position_soi = self.position / self.quad.distance_maximale

        # return np.concatenate([np.array([distance_proie, angle_proie, distance_obstacle, angle_obstacle]), position_soi])
        # contact_obstacle = 0
        # if self.contact_obstacle():
        #     contact_obstacle = 1

        return np.array([
            distance_predateur,
            angle_predateur,
            vecteur_predateur[0] / self.quad.distance_maximale,
            vecteur_predateur[1] / self.quad.distance_maximale,
            distance_obstacle,
            angle_obstacle,
            self.contact_obstacle(),
            vecteur_obstacle[0] / self.quad.distance_maximale,
            vecteur_obstacle[1] / self.quad.distance_maximale,
            angle_vitesse,
            self.vitesse[0] / self.vitesse_max,
            self.vitesse[1] / self.vitesse_max,
            self.position[0] / self.quad.distance_maximale,
            self.position[1] / self.quad.distance_maximale,
        ])