from ray.rllib import MultiAgentEnv
from gymnasium import spaces
from gymnasium.utils import seeding
import numpy as np

from environnement.jeu import Jeu
from environnement.quad import Quad
from environnement.proie import Proie
from environnement.predateur import Predateur
from environnement.obstacle import Obstacle


class ChaseTag(MultiAgentEnv):
    def __init__(self, config):
        super().__init__()
        self._agent_ids = {'proie', 'predateur'}
        self.observation_space = {
            'proie': spaces.Box(low=-np.inf, high=np.inf, shape=(6,), dtype=np.float32),
            'predateur': spaces.Box(low=-np.inf, high=np.inf, shape=(6,), dtype=np.float32),
        }
        self.action_space = {
            'proie': spaces.Box(low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32),
            'predateur': spaces.Box(low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32),
        }
        self.seed()

        dimension = config.get('dimension', np.array([300, 300]))
        nombre_obstacles = config.get('nombre_obstacles', 1)
        tailles_obstacles = config.get('tailles_obstacles', 40)
        nombre_proies = config.get('nombre_proies', 1)
        taille_proies = config.get('taille_proies', 10)
        vitesse_maximale_proies = config.get('vitesse_maximale_proies', 5)
        acceleration_proies = config.get('acceleration_proies', 1)
        nombre_predateurs = config.get('nombre_predateurs', 1)
        taille_predateurs = config.get('taille_predateurs', 10)
        vitesse_maximale_predateurs = config.get('vitesse_maximale_predateurs', 5)
        acceleration_predateurs = config.get('acceleration_predateurs', 1)
        temps_jeu_maximum = config.get('temps_jeu_maximum', 200)
        intervalle_temporel = config.get('intervalle_temporel', 1)
        self.rendre_graphiquement = config.get('render_env', False)
        fps = config.get('fps', 30)

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

        self.jeu: Jeu = Jeu(
            quad,
            predateurs,
            proies,
            temps_jeu_maximum,
            intervalle_temporel,
            self.rendre_graphiquement,
            fps,
        )
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self, seed=None, options=None):
        self.jeu.reinitialisation()
        obs = {
            'proie': self.jeu.quad.proies[0].observation(),
            'predateur': self.jeu.quad.predateurs[0].observation(),
        }
        return obs, {}

    def step(self, action):
        self.jeu.increment_apprentissage_renforecement(action)
        obs = {
            'proie': self.jeu.quad.proies[0].observation(),
            'predateur': self.jeu.quad.predateurs[0].observation(),
        }
        bonus_predateur = 0
        bonus_proie = 0
        if self.jeu.verification_victoire_perdateurs():
            bonus_predateur = 1 - (self.jeu.temps_jeu_courant/self.jeu.temps_jeu_maximum)
        if self.jeu.predateurs[0].contact_obstacle():
            bonus_predateur = - 2/self.jeu.nombre_actions_max
        if self.jeu.proies[0].contact_obstacle():
            bonus_proie = - 2/self.jeu.nombre_actions_max

        reward = {
            'proie': 1/self.jeu.nombre_actions_max,
            'predateur': bonus_predateur - (1/self.jeu.nombre_actions_max) * (np.linalg.norm(self.jeu.predateurs[0].position - self.jeu.proies[0].position) / self.jeu.quad.distance_maximale),  #-1/self.jeu.nombre_actions_max,
        }
        if self.rendre_graphiquement:
            print('reward : ' + str(bonus_predateur - (1/self.jeu.nombre_actions_max) * (np.linalg.norm(self.jeu.predateurs[0].position - self.jeu.proies[0].position) / self.jeu.quad.distance_maximale)))
        terminated = {
            '__all__': self.jeu.verification_victoire_proies() or self.jeu.verification_victoire_perdateurs(),
            'proie': False,
            'predateur': False,
        }
        truncated = {
            '__all__': False,
            'proie': False,
            'predateur': False,
        }

        return obs, reward, terminated, truncated, {}
