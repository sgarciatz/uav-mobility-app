import unittest
from uav_mobility_app.gym_envs.envs.NetworkEnv import NetworkEnv
from uav_mobility_app.gym_envs.entities.Network import Network
from uav_mobility_app.gym_envs.entities.NetworkNode import NetworkNode
from uav_mobility_app.gym_envs.entities.NetworkDevice import NetworkDevice
from uav_mobility_app.gym_envs.entities.NetworkLink import NetworkLink
from uav_mobility_app.gym_envs.enums.NetworkNodeType import NetworkNodeType
from uav_mobility_app.gym_envs.enums.NetworkDeviceType import NetworkDeviceType
from uav_mobility_app.gym_envs.entities.ExtendedNetworkLink import ExtendedNetworkLink
from gymnasium.spaces import Space
import numpy as np
from pathlib import Path


class test_NetworkEnv(unittest.TestCase):


    def test_initialization(self):
        """Test that the NetworkEnv is initialized as expected when
        network_00.json is the environment used.
        """
        n_actions = 5
        net: Network = Network(Path.cwd().joinpath("input", "network_00.json"))
        net_env = NetworkEnv(network=net,
                             n_actions=n_actions,
                             render_mode=None)
        obs_space: Space = net_env.get_wrapper_attr("observation_space")
        action_space: Space = net_env.get_wrapper_attr("action_space")
        self.assertEqual(obs_space.shape[0], n_actions * 3)
        self.assertEqual(action_space.n, n_actions)
        self.assertEqual(net_env.get_wrapper_attr("_dev"), None)
        self.assertEqual(len(net_env.get_wrapper_attr("_path")), 0)

    def test_reset(self):
        """Test that when reset is called all links are
        empty, their resources are free, all Devices, except the
        selected one, are inactive and that the observation obtained is
        consistent to the available links for the selected
        NetworkDevice."""
        n_actions = 5
        net: Network = Network(Path.cwd().joinpath("input", "network_00.json"))
        net_env = NetworkEnv(network=net,
                             n_actions=n_actions,
                             render_mode=None)
        obs, _ = net_env.reset(seed=None, options=None)
        max_c: float = net_env.get_wrapper_attr("_obs_space").high[0]
        max_l: float = net_env.get_wrapper_attr("_obs_space").high[1]
        min_t: float = net_env.get_wrapper_attr("_obs_space").low[2]
        self.assertGreater(max_c, obs[0][0])
        self.assertGreater(max_l, obs[0][1])
        self.assertGreater(obs[0][2], min_t)
        for option in obs[1:]:
            self.assertEqual(max_c, option[0])
            self.assertEqual(max_l, option[1])
            self.assertEqual(min_t, option[2])
        for l in net.network_links:
            self.assertEqual(l.available_throughput, l.max_throughput)
            self.assertEqual(len(l.routed_flows), 0)
        selected_dev: NetworkDevice = net_env.get_wrapper_attr("_dev")
        self.assertTrue(selected_dev.is_active)
        for d in set(net.network_devices) - set([selected_dev]):
            self.assertFalse(d.is_active)

    def test_hard_reset(self):
        """Test that when the reset function is called with the hard
        reset flag, the Network is cleared, i.e., the NetworkDevices'
        paths are deallocated, they are set to inactive and all
        NetworkLinks' resources are freed.
        """
        n_actions = 5
        net: Network = Network(Path.cwd().joinpath("input", "network_00.json"))
        net_env = NetworkEnv(network=net,
                             n_actions=n_actions,
                             render_mode=None)
        net_env.reset()
        terminated = False
        while (not terminated):
            obs, reward, terminated, _, _ = net_env.step(0)
        network_link_path: list[NetworkLink] = []
        device: NetworkDevice = net_env.get_wrapper_attr("_dev")
        self.assertTrue(device.is_active)
        for l in net_env.get_wrapper_attr("_path"):
            link: NetworkLink = l[2]["data"]
            self.assertGreater(link.max_throughput, link.available_throughput)
            network_link_path.append(link)
        net_env.reset(options={"hard_reset": True})
        self.assertFalse(device.is_active)
        for l in network_link_path:
            self.assertEqual(link.max_throughput, link.available_throughput)
            self.assertEqual(len(l.routed_flows), 0)


    def test_step(self):
        """Test that a step is consistent. That is, the chosen
        NetworkLink is added to the self._path list and that the return
        values are correct: reward 0 if the state is not terminal and x
        otherwise, the observation represents the link of the selected
        NetworkLink. The info is a empty dict for the time being.
        """
        n_actions = 5
        net: Network = Network(Path.cwd().joinpath("input", "network_00.json"))
        net_env = NetworkEnv(network=net,
                             n_actions=n_actions,
                             render_mode=None)
        net_env.reset()
        device: NetworkDevice = net_env.get_wrapper_attr("_dev")
        network_link_path = net_env.get_wrapper_attr("_path")
        terminated = False
        expected_links: int = 1
        self.assertEqual(len(network_link_path), expected_links)
        expected_links += 1
        while (not terminated):
            _, _, terminated, _, _ = net_env.step(0)
            self.assertEqual(len(network_link_path), expected_links)
            expected_links += 1


    def test_step_padded_action(self):
        """Test that when a "false" padded link is chosen as an action,
        no NetworkLink is added to the self._path list.
        """
        n_actions = 5
        net: Network = Network(Path.cwd().joinpath("input", "network_00.json"))
        net_env = NetworkEnv(network=net,
                             n_actions=n_actions,
                             render_mode=None)
        net_env.reset()
        device: NetworkDevice = net_env.get_wrapper_attr("_dev")
        network_link_path = net_env.get_wrapper_attr("_path")
        terminated = False
        expected_links: int = 1
        self.assertEqual(len(network_link_path), expected_links)
        n_actions: int = net_env.get_wrapper_attr("action_space").n
        for i in range(5):
            net_env.step(n_actions-1)
            self.assertEqual(len(network_link_path), expected_links)
        _, _, terminated, _, _ = net_env.step(0)
        expected_links += 1
        self.assertEqual(len(network_link_path), expected_links)
        for i in range(5):
            net_env.step(n_actions-1)

            self.assertEqual(len(network_link_path), expected_links)

    def test_obs(self):
        """Test that the observations are consistent with the subyacent
        Network instance and that if there are less than self._actions
        available NetworkLinks, the remaining ones are padded with fake
        links.
        """
        n_actions = 5
        net: Network = Network(Path.cwd().joinpath("input", "network_00.json"))
        net_env = NetworkEnv(network=net,
                             n_actions=n_actions,
                             render_mode=None)
        uav: NetworkDevice =  list(filter(
            lambda u: u.name == "uav_00",
            net.uavs))[0]
        net_env._dev = uav
        link= list(net_env._network.out_edges(net_env._dev, data=True))[0]
        net_env._path.append(link)
        max_c: float = net_env.get_wrapper_attr("_obs_space").high[0]
        max_l: float = net_env.get_wrapper_attr("_obs_space").high[1]
        min_t: float = net_env.get_wrapper_attr("_obs_space").low[2]
        obs = net_env._get_obs()
        self.assertEqual(len(obs), n_actions)
        self.assertGreater(max_c, obs[0][0])
        self.assertGreater(max_l, obs[0][1])
        self.assertGreater(obs[0][2], min_t)
        for option in obs[1:]:
            self.assertEqual(max_c, option[0])
            self.assertEqual(max_l, option[1])
            self.assertEqual(min_t, option[2])

    def test_get_next_links(self):
        """Check that the adjacent NetworkLinks to a given NetworkNode
        that lead to the NetworkNode of NetworkNodeType.GW are returned.
        """
        n_actions = 5
        net: Network = Network(Path.cwd().joinpath("input", "network_00.json"))
        net_env = NetworkEnv(network=net,
                             n_actions=n_actions,
                             render_mode=None)
        link: ExtendedNetworkLink = list(filter(
            lambda l: l[2]["data"].id == 119,
            list(net.edges(data=True))))[0]
        net_env._path.append(link)
        next_links: list[ExtendedNetworkLink] = net_env._get_next_links()
        print(next_links)
        link_0: ExtendedNetworkLink = list(filter(
            lambda l: l[2]["data"].id == 107,
            list(net.edges(data=True))))[0]
        link_1: ExtendedNetworkLink = list(filter(
            lambda l: l[2]["data"].id == 110,
            list(net.edges(data=True))))[0]
        self.assertEqual(link_0, next_links[0])
        self.assertEqual(link_1, next_links[1])
        self.assertEqual((0, 0, 0), next_links[2])
        self.assertEqual((0, 0, 0), next_links[3])
        self.assertEqual((0, 0, 0), next_links[4])
