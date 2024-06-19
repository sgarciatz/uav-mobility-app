from gymnasium import Wrapper, Env
from pathlib import Path

class FlattenObservationSpace(Wrapper):

    def __init__(self, env: Env):
        super().__init__(env)
        print(self.observation_space)

    def reset(self,
              *,
              seed: int | None = None,
              options: dict | None = None) -> tuple:
        """Flattens the observation returned by the subjacent Env.

        Args:
            seed (int | None, optional): The seed to provide
            reproducibility. Defaults to None.
            options (dict | None, optional): no use for options.
            Defaults to None.

        Returns:
            tuple: The flattened observation and additional info.
        """
        obs, info = super().reset(seed=seed, options=options)
        obs = obs.flatten(order="C")
        return obs, info

    def step(self, action: "Any") -> tuple:
        """Flattens the observation returned by the subjacent Env.

        Args:
            action (Any): The action to perform.

        Returns:
            Any: The flattened observation and additional info.
        """
        obs, reward, terminated, truncated, info = super().step(action=action)
        obs = obs.flatten(order="C")
        return obs, reward, terminated, truncated, info
