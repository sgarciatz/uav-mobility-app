from typing import Any
import random
import gymnasium as gym
import numpy as np
from gymnasium import spaces
from gymnasium.spaces.utils import flatten_space
from uav_mobility_app.gym_envs.entities.Network import Network
from uav_mobility_app.gym_envs.entities.NetworkDevice import NetworkDevice
from uav_mobility_app.gym_envs.entities.NetworkNode import NetworkNode
from uav_mobility_app.gym_envs.entities.NetworkLink import NetworkLink
from uav_mobility_app.gym_envs.enums.NetworkNodeType import NetworkNodeType


class NetworkEnv(gym.Env):


    def __init__(self,
                 network: Network,
                 render_mode:str = None) -> None:
        """_summary_

        Args:
            render_mode (str, optional): _description_. Defaults to None.
        """
        self._network: Network = network
        self._actions = 3
        self.action_space = spaces.Discrete(self.actions,
                                            start=0)
        self._obs_space_0 = spaces.Box(low=np.array([0.0, 0.0, 0.0]),
                                      high=np.array([1.0, 20.0, 1000.0]),
                                      shape=(3,))
        self._obs_space_1 = spaces.Box(low=np.array([0.0, 0.0, 0.0]),
                                      high=np.array([1.0, 20.0, 1000.0]),
                                      shape=(3,))
        self._obs_space_2 = spaces.Box(low=np.array([0.0, 0.0, 0.0]),
                                      high=np.array([1.0, 20.0, 1000.0]),
                                      shape=(3,))
        self.observation_space = flatten_space((self._obs_space_0,
                                                self._obs_space_1,
                                                self._obs_space_2))
        self._dev: NetworkDevice = None
        self._link: tuple[NetworkNode,
                          NetworkNode,
                          dict[str, NetworkDevice]] = None
        self._path: list[tuple[NetworkNode,
                               NetworkNode,
                               dict[str, NetworkDevice]]] = []

    def reset(self,
              *,
              seed: int | None = None,
              options: dict | None = None) -> tuple:
        """Resets the enviroment.

        Args:
            seed (int | None, optional): The seed to provide
            reproducibility. Defaults to None.
            options (dict[str, Any] | None, optional): No use for
            options yet. Defaults to None.

        Returns:
            tuple: The observations and additional info.
        """
        if (seed != None):
            random.seed(seed)
        if (options["hard_reset"] == True):
            for d in self._network.network_devices:
                dev_path = self._network.get_path_device(d)
                self._network.free_path_device(d, dev_path)

        uav_or_cam = random.randint(0, 1)
        if (uav_or_cam == 0):
            self._dev = self._network.generate_cam_event()
        else:
            self._dev = self._network.generate_uav_event()
        obs = self._get_obs()
        info = self._get_info()
        return obs, info

    def step(self, action: Any) -> tuple:
        """Performs and action in the current state and transitions into
        a new state.

        Args:
            action (Any): The action to perform

        Returns:
            tuple: The observations and additional info.
        """

        # Based on the action, select the corresponding path
        next_link = self._network.get_next_link(self._dev, self._link, action)
        dst_node: NetworkNode = next_link(1)
        link: NetworkLink = next_link(2)["data"]
        self._path.append(link)

        # Check if we are in a terminal state
        terminated = False
        if (dst_node.node_type == NetworkNodeType.GW):
            terminated = True
        obs = self._get_obs()
        info = self._get_info()
        reward = self._get_reward()
        return obs, reward, terminated, False, info

    def _get_info(self) -> dict:
        """Get detailed information about the environment's current
        state.

        Returns:
            dict: The information about the environment's current
            state.
        """
        return self._get_obs()

    def _get_obs(self):
        """Get the information that is observable by the agents about
        the environment's current state.

        Returns:
            dict: The information that is observable by the agents about
        the environment's current state.
        """
        links: list[NetworkLink] = self._network.get_next_links(self._dev,
                                                                self._path[-1],
                                                                self._actions)
        obs: list = []
        for link in links:
            c = 0.0
            if (self._dev in link.routed_flows):
                c = 1.0
            l = link.delay
            t = link.available_throughput
            obs.append([c,l,t])

        return np.array(obs, dtype=np.float64)

    def _get_reward(self):
        """Get the reward associated to the actions carried out during
        the episode. It is calculated as the sum of the number of
        changes scaled to [0, 1] and the marginal delay, also scaled.
        """
        delay = 0
        changes = 0
        for (u, v, l) in self._path:
            l: NetworkLink = l["data"]
            delay += l.delay
            if (self._dev not in l.routed_flows):
                changes += 1
        delay = (self._dev.delay_req - delay) / self._dev.delay_req
        changes = (1 - changes / len(self._path))
        reward = changes * 0.7 + delay * 0.3
        return reward