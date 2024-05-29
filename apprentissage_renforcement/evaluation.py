import ray
from ray.rllib.algorithms.algorithm import AlgorithmConfig, Algorithm
from environnement_apprentissage_renforcement import ChaseTag
from ray.tune.registry import register_env
from itertools import product
import warnings
import logging
from datetime import datetime

if __name__ == '__main__':
    if not ray.is_initialized():
        ray.init(local_mode=True, logging_level=logging.ERROR)

    warnings.filterwarnings("ignore")

    register_env(name='ChaseTag', env_creator=ChaseTag)

    path_checkpoint: str = '/home/malaarabiou/Programming_Projects/Pycharm_Projects/Anthony_Project/apprentissage_renforcement/resultat/PPO_2024-05-25_22-18-04/PPO_ChaseTag_e4363_00000_0_2024-05-25_22-18-04/checkpoint_000304'
    algorithm: Algorithm = Algorithm.from_checkpoint(path_checkpoint)
    algorithm_config: AlgorithmConfig = Algorithm.get_config(algorithm).copy(copy_frozen=False)

    params = {
        'nombre_obstacles': [1, 2, 3, 4, 5],
        'vitesse_maximale_proies': [0.1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
        'acceleration_proies': [0.5, 0.75, 1, 1.25, 1.5],
        'taille_proies': [5, 10, 15, 20],
        # 'vitesse_maximale_predateurs': [0.1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        # 'acceleration_predateurs': [0.5, 1, 1.5],
    }

    # Générer toutes les combinaisons possibles de valeurs
    keys, values = zip(*params.items())
    combinations = [dict(zip(keys, v)) for v in product(*values)]

    # Obtenir la date actuelle et formater le nom du fichier
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"configurations_{current_date}.txt"

    with open(filename, 'w') as file:
        # Afficher les dictionnaires de configuration générés
        for config in combinations:
            # print(config)
            file.write(str(config) + '\n')

            number_iteration: int = 100
            algorithm_config.environment(
                env_config=config,
            )
            algorithm_config.evaluation(
                evaluation_duration=number_iteration,
                evaluation_config=config,
            )
            algorithm_config.rollouts(
                num_rollout_workers=1,
                num_envs_per_worker=1,
            )
            algorithm_config.env_config = config
            algorithm: Algorithm = algorithm_config.build()
            algorithm.restore(path_checkpoint)

            # for i in range(number_iteration):
            evaluation_result = algorithm.evaluate()
            # print(evaluation_result['env_runners']['policy_reward_mean']['proie'])
            file.write(str(evaluation_result['env_runners']['policy_reward_mean']['proie']) + '\n')
            # print()
            file.write('\n')
