import ray
from ray.rllib.algorithms.algorithm import AlgorithmConfig, Algorithm
from environnement_apprentissage_renforcement import ChaseTag
from ray.tune.registry import register_env

if __name__ == '__main__':
    if not ray.is_initialized():
        ray.init(local_mode=True)

    register_env(name='ChaseTag', env_creator=ChaseTag)

    path_checkpoint: str = '/home/malaarabiou/Programming_Projects/Pycharm_Projects/Anthony_Project/apprentissage_renforcement/resultat/PPO_2024-05-25_22-18-04/PPO_ChaseTag_e4363_00000_0_2024-05-25_22-18-04/checkpoint_000304'
    algorithm: Algorithm = Algorithm.from_checkpoint(path_checkpoint)
    algorithm_config: AlgorithmConfig = Algorithm.get_config(algorithm).copy(copy_frozen=False)

    config = {
        'render_env': True,
        'vitesse_maximale_proies': 10,
        'vitesse_maximale_predateurs': 2.5,
    }

    algorithm_config.environment(
        env_config=config,
    )
    algorithm_config.evaluation(
        evaluation_duration=1,
        evaluation_config=config,
    )
    algorithm_config.rollouts(
        num_rollout_workers=1,
        num_envs_per_worker=1,
    )
    algorithm_config.env_config = config

    algorithm: Algorithm = algorithm_config.build()
    algorithm.restore(path_checkpoint)
    number_iteration: int = 1000
    for i in range(number_iteration):
        evaluation_result = algorithm.evaluate()
