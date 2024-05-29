import time
import pygame
import numpy as np


def angle_vecteur(angle):
    # Calculer les composants x et y du vecteur
    x = np.cos(angle)
    y = np.sin(angle)

    # Retourner le vecteur unitaire
    return np.concatenate([x, y])

class Jeu:
    def __init__(
        self,
        quad,
        predateurs,
        proies,
        temps_jeu_maximum,
        intervalle_temporel,
        rendre_graphiquement,
        fps,
    ):
        self.quad = quad
        self.predateurs = predateurs
        self.proies = proies
        self.personnages = self.predateurs + self.proies
        self.temps_jeu_courant: float
        self.temps_jeu_maximum = temps_jeu_maximum
        self.intervalle_temporel = intervalle_temporel
        self.nombre_actions_max = self.temps_jeu_maximum / self.intervalle_temporel

        self.rendre_graphiquement = rendre_graphiquement
        self.fps = fps
        self.fenetre = None
        pygame.display.set_caption('Chase Tag')

        self.reinitialisation()

    def reinitialisation(self):
        self.temps_jeu_courant = 0
        self.quad.reinitialisation()

        for personnage in self.personnages:
            personnage.reinitialisation()

    def increment(self):
        self.temps_jeu_courant += self.intervalle_temporel

        for personnage in self.personnages:
            if personnage.en_jeu:
                personnage.agit(self.intervalle_temporel)

        if self.rendre_graphiquement:
            self.rendu_graphique()

    def increment_apprentissage_renforecement(self, action):
        self.temps_jeu_courant += self.intervalle_temporel

        # self.proies[0].accelerer(angle_vecteur(action['proie'] * np.pi))
        self.proies[0].accelerer(action['proie'])
        self.proies[0].deplace(self.intervalle_temporel)

        # self.predateurs[0].accelerer(angle_vecteur(action['predateur'] * np.pi))
        self.predateurs[0].accelerer(action['predateur'])
        self.predateurs[0].deplace(self.intervalle_temporel)

        if self.rendre_graphiquement:
            self.rendu_graphique()

    def rendu_graphique(self):
        if self.fenetre is None:
            self.fenetre = pygame.display.set_mode(self.quad.dimension)

        pygame.display.flip()
        time.sleep(1 / self.fps)
        self.fenetre.fill((0, 0, 0))

        for personnage in self.personnages:
            if personnage.en_jeu == True:
                personnage.rendu_graphique(self.fenetre)

        self.quad.rendu_graphique(self.fenetre)

        # print('proie obs : ' + str(self.proies[0].observation()))
        print('predateur obs : ' + str(self.predateurs[0].observation()))
        pass

    def verification_victoire_proies(self):
        if self.temps_jeu_courant > self.temps_jeu_maximum:
            return True
        else:
            return False

    def verification_victoire_perdateurs(self):
        victoire = True

        for proie in self.proies:
            if proie.en_jeu == True:
                victoire = False

        return victoire