import math
import numpy as np

from environnement.personnage import Personnage
from environnement.proie import Proie


class Predateur(Personnage):
    def __init__(self, quad, taille, vitesse_max, acceleration):
        super().__init__(quad, taille, vitesse_max, acceleration)
        self.couleur = (255, 0, 0)
        self.quad.predateurs.append(self)

    def agit(self, intervalle_temporel):
        self.accelerer(self.direction_traque())
        self.deplace(intervalle_temporel)

    def direction_traque(self):
        direction = np.array([0, 0], dtype=np.float64)
        position_cible = self.position_proie_plus_proche()

        coef_traque = 1

        if position_cible is not None:
            vecteur_traque = position_cible - self.position
            direction_traque = vecteur_traque / np.linalg.norm(vecteur_traque)
            direction += direction_traque * coef_traque

        if np.linalg.norm(direction) > 0:
            direction / np.linalg.norm(direction)
        return direction

    def position_proie_plus_proche(self):
        distance_plus_proche = math.inf
        position = None

        for proie in self.quad.proies:
            vecteur = self.position - proie.position
            distance = np.linalg.norm(vecteur) - proie.taille

            if distance_plus_proche > distance and proie.en_jeu:
                distance_plus_proche = distance
                position = proie.position

        if position is None:
            position = np.array([-1, -1])

        return position

    def controle_collision(self):
        collision = False
        for obstacle in self.quad.obstacles:
            if obstacle.collision(self) and obstacle != self:
                collision = True

        for personnage in self.quad.personnages:
            if personnage.en_jeu and personnage.collision(self) and personnage != self:
                collision = True
                if isinstance(personnage, Proie):
                    personnage.en_jeu = False

        return collision

    def observation(self):
        # position_proie = self.position_proie_plus_proche() - self.position
        # position_obstacle = self.position_obstacle_plus_proche() - self.position
        # position_soi = self.position
        # return np.concatenate([position_proie, position_obstacle, position_soi]) / self.quad.distance_maximale

        vecteur_proie = self.position_proie_plus_proche() - self.position
        distance_proie = np.linalg.norm(vecteur_proie) / self.quad.distance_maximale
        angle_proie = np.arctan2(vecteur_proie[0], vecteur_proie[1]) / np.pi

        vecteur_obstacle = self.position_obstacle_plus_proche() - self.position
        distance_obstacle = np.linalg.norm(vecteur_obstacle) / self.quad.distance_maximale
        angle_obstacle = np.arctan2(vecteur_obstacle[0], vecteur_obstacle[1]) / np.pi

        angle_vitesse = np.arctan2(self.vitesse[0], self.vitesse[1]) / np.pi

        # position_soi = self.position / self.quad.distance_maximale

        # return np.concatenate([np.array([distance_proie, angle_proie, distance_obstacle, angle_obstacle]), position_soi])
        # contact_obstacle = 0
        # if self.contact_obstacle():
        #     contact_obstacle = 1
        # print(contact_obstacle)
        # print('vecteur_obstacle : ' + str(vecteur_obstacle))
        # print('distance_obstacle : ' + str(distance_obstacle))

        return np.array([
            distance_proie,
            angle_proie,
            vecteur_proie[0] / self.quad.distance_maximale,
            vecteur_proie[1] / self.quad.distance_maximale,
            distance_obstacle,
            angle_obstacle,
            self.contact_obstacle(),
            vecteur_obstacle[0] / self.quad.distance_maximale,
            vecteur_obstacle[1] / self.quad.distance_maximale,
            angle_vitesse,
            self.vitesse[0]/self.vitesse_max,
            self.vitesse[1]/self.vitesse_max,
            self.position[0]/self.quad.distance_maximale,
            self.position[1]/self.quad.distance_maximale,
        ])
