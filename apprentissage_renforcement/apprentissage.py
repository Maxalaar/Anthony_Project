import os
import ray
from ray import air, tune
from ray.rllib.algorithms.ppo import PPOConfig, PPO
from ray.tune.registry import register_env
from ray.rllib.policy.policy import PolicySpec
from gymnasium import spaces
import numpy as np

from environnement_apprentissage_renforcement import ChaseTag

# tensorboard --host=0.0.0.0 --port=6006 --logdir /home/malaarabiou/Programming_Projects/Pycharm_Projects/Anthony_Project/apprentissage_renforcement/resultat
if __name__ == '__main__':
    ray.init(local_mode=False)
    register_env(name='ChaseTag', env_creator=ChaseTag)

    def select_policy(agent_id, episode, worker, **kwargs) -> str:
        return agent_id

    algorithm_configuration = (
        PPOConfig()
        .environment(env='ChaseTag', env_config={})
        .framework('torch')
        .training(
            model={
                'fcnet_hiddens': [64, 64, 64],
                # 'use_lstm': True,
            },
        )
        .multi_agent(
            policies={
                'proie': PolicySpec(observation_space=spaces.Box(low=-1, high=1, shape=(14,), dtype=np.float32), action_space=spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32), config={}),
                'predateur': PolicySpec(observation_space=spaces.Box(low=-1, high=1, shape=(14,), dtype=np.float32), action_space=spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32), config={}),
            },
            policy_mapping_fn=select_policy,
        )
        .rollouts(
            num_rollout_workers=10,
            num_envs_per_worker=1,
            batch_mode='complete_episodes',
        )
        .evaluation(
            evaluation_num_workers=1,
            evaluation_interval=2,
        )
        .resources(
            num_learner_workers=2,
        )
    )

    tuner = tune.Tuner(
        trainable=PPO,
        param_space=algorithm_configuration,
        run_config=air.RunConfig(
            storage_path=os.path.join(os.getcwd(), 'resultat/'),
            stop={
                'time_total_s': 60 * 60 * 24 * 7,
            },
            checkpoint_config=air.CheckpointConfig(
                num_to_keep=1,
                checkpoint_score_attribute='episode_reward_mean',
                checkpoint_score_order='max',
                checkpoint_frequency=10,
                checkpoint_at_end=True,
            )
        ),
    )

    tuner.fit()
