from typing import Any
import random
import gymnasium as gym
import numpy as np
from pathlib import Path
from gymnasium import spaces
from gymnasium.spaces.utils import flatten_space
from network_envs.entities.Network import Network
from network_envs.entities.Network import ExtendedNetworkLink
from network_envs.entities.NetworkDevice import NetworkDevice
from network_envs.entities.NetworkNode import NetworkNode
from network_envs.entities.NetworkLink import NetworkLink
from network_envs.enums.NetworkNodeType import NetworkNodeType


class NetworkEnv(gym.Env):


    def __init__(self,
                 configuration: Path,
                 n_actions: int = 3,
                 hard_reset_period: int = 100,
                 render_mode:str = None) -> None:
        """Initializaes the NetworkEnv. This method is designed to be
        callable by gym.make(...).

        Args:
            configuration (Path): The file that contains the
            configuration for the enviroment.
            n_actions (int): The number of links that the agent can
            choose at a given step. Defaults to 3.
            hard_reset_period (int): The number of episodes to carry out
            before performing a hard reset. Defaults to 100.
            render_mode (str, optional): No use for this feature yet.
            Defaults to None.
        """
        self._hard_reset_period = hard_reset_period
        self._hard_reset_counter = 1
        self._network: Network = Network(configuration=configuration)
        self.action_space = spaces.Discrete(n_actions,
                                            start=0)

        self._obs_space = spaces.Box(low=np.array([0.0, 0.0, 0.0]),
                                      high=np.array([1.0+1.0,
                                                     20.0+1.0,
                                                     1000.0+1.0]),
                                      shape=(3,))
        self.observation_space =\
            spaces.Tuple((self._obs_space for _ in range(n_actions)))
        self.observation_space = flatten_space(self.observation_space)
        self._dev: NetworkDevice = None
        self._path: list[tuple[NetworkNode,
                               NetworkNode,
                               dict[str, NetworkDevice]]] = []

    def reset(self,
              *,
              seed: int | None = None,
              options: dict | None = None) -> tuple:
        """Resets the enviroment. If enough episodes have been carried
        out, a hard reset shall be executed, which deallocates all
        resources and set all device to inactive.

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
        if (self._hard_reset_counter >= self._hard_reset_period):
            self._hard_reset_counter = 1
            for d in self._network.network_devices:
                dev_path = self._network.get_path_device(d)
                self._network.free_path_device(d, dev_path)
                d.is_active = False
        else:
            self._hard_reset_counter += 1
        uav_or_cam = random.randint(0, 1)
        if (uav_or_cam == 0):
            self._dev = self._network.generate_cam_event()
        else:
            self._dev = self._network.generate_uav_event()
        self._path = []
        link= list(self._network.out_edges(self._dev, data=True))[0]
        self._path.append(link)
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
        next_link = self._get_next_links()[action]
        dst_node: NetworkNode = next_link[1]
        terminated = False
        reward = 0
        # Check if a "false" NetworkLink is selected
        if (isinstance(dst_node, NetworkNode)):
            self._path.append(next_link)
        # Check if we are in a terminal state
            if (dst_node.node_type == NetworkNodeType.GW):
                reward = self._get_reward()
                terminated = True
                #TODO Allocate resources for the path
                path: list[NetworkLink] = []
                for (_, _, l) in self._path:
                    path.append(l["data"])
                self._network.assign_path_to_device(self._dev, path)
        # print("SANTIAGO")
        # for l in self._get_next_links():
        #     print(l[0])
        #     print(l[1])
        #     print(l[2])
        # print("GARCIA GIL")

        obs = self._get_obs()
        info = self._get_info()
        return obs, reward, terminated, False, info

    def _get_info(self) -> dict:
        """Get detailed information about the environment's current
        state.

        Returns:
            dict: The information about the environment's current
            state.
        """
        return {}

    def _get_obs(self):
        """Get the information that is observable by the agents about
        the environment's current state.

        Returns:
            dict: The information that is observable by the agents about
        the environment's current state.
        """
        # Get all the possible links
        next_links = self._get_next_links()
        observations = []
        for (_, _, l) in next_links:
            if (isinstance(l, dict)):
                link: NetworkLink = l["data"]
                c = 1.0
                if (self._dev in link.routed_flows):
                    c = 0.0
                l = link.delay
                t = link.available_throughput
            else:
                c = self._obs_space.high[0]
                l = self._obs_space.high[1]
                t = self._obs_space.low[2]
            observations.append([c,l,t])
        remaining_links = len(observations) < self.action_space.n
        if (remaining_links > 0):
            for _ in range(remaining_links):
                observations.append([self._obs_space.low[0],
                                     self._obs_space.low[1],
                                     self._obs_space.low[2]])
        observations.sort(key=lambda obs: (obs[0],
                                           obs[1],
                                           self._obs_space.high[2] - obs[2]))
        return np.array(observations, dtype=np.float64)

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

    def _get_next_links(self) -> list[ExtendedNetworkLink]:
        """Return the self.actions next edges that lead to the gateway.
        To this end, all the possible links are orderded and filtered.
        If there are less than self._actions, the remaining one are
        padded (action masking).

        Returns:
            list[ExtendedNetworkLink]: The possible next NetworkLink
            that may be chosen (padded if needed).
        """
        next_links = self._network.get_next_link(self._path[-1])
        remainin_links = self.action_space.n - len(next_links)
        if (remainin_links > 0):
            for _ in range(remainin_links):
                next_links.append((0,0,0))
        return next_links
