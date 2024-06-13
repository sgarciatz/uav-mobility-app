from typing import Any
import random
import gymnasium as gym
import numpy as np
from gymnasium import spaces
from gymnasium.spaces.utils import flatten_space
from uav_mobility_app.gym_envs.entities.Network import Network
from uav_mobility_app.gym_envs.entities.Network import ExtendedNetworkLink
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
        self.action_space = spaces.Discrete(self._actions,
                                            start=0)

        self._obs_space = spaces.Box(low=np.array([0.0, 0.0, 0.0]),
                                      high=np.array([1.0+1.0,
                                                     20.0+1.0,
                                                     1000.0+1.0]),
                                      shape=(3,))
        self.observation_space = spaces.Tuple((self._obs_space for _ in range(self._actions)))
        self.observation_space = flatten_space(self.observation_space)
        self._dev: NetworkDevice = None
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
        if (options != None):
            for d in self._network.network_devices:
                dev_path = self._network.get_path_device(d)
                self._network.free_path_device(d, dev_path)

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
        self._path.append(next_link)
        # Check if we are in a terminal state
        terminated = False
        reward = 0
        if (dst_node.node_type == NetworkNodeType.GW):
            reward = self._get_reward()
            terminated = True
            #TODO Allocate resources for the path
            path: list[NetworkLink] = []
            for (_, _, l) in self._path:
                path.append(l["data"])
            self._network.assign_path_to_device(self._dev, path)
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
                c = self._obs_space.high[1]
                l = self._obs_space.high[1]
                t = self._obs_space.low[2]
            observations.append([c,l,t])
        remaining_links = len(observations) < self._actions
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
        remainin_links = self._actions - len(next_links)
        if (remainin_links > 0):
            for _ in range(remainin_links):
                next_links.append((0,0,0))
        return next_links

if __name__ == "__main__":
    from pathlib import Path
    import matplotlib.pyplot as plt
    my_net = Network(Path("/home/santiago/Documents/Trabajo/Workspace/uav-mobility-app/input/network_00.json"))
    my_net_env = NetworkEnv(my_net)
    for _ in range(20):
        obs, _ = my_net_env.reset()
        obs, reward, terminated, _, info = my_net_env.step(0)
        obs, reward, terminated, _, info = my_net_env.step(0)
        obs, reward, terminated, _, info = my_net_env.step(0)

        my_net.show_network_info()
        plt.show()
