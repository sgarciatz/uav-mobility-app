from gymnasium.envs.registration import register

register(
    id="network_envs/NetworkEnv-v0",
    entry_point="network_envs.envs:NetworkEnv",
    max_episode_steps=10,
    reward_threshold=None,
    nondeterministic=False,
    order_enforce=True,
    autoreset=False,
)
