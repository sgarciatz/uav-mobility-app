import unittest
from pathlib import Path
import json
from uav_mobility_app.gym_envs.entities.NetworkLink import NetworkLink
from uav_mobility_app.gym_envs.entities.NetworkDevice import NetworkDevice
from uav_mobility_app.gym_envs.enums.NetworkDeviceType import NetworkDeviceType
from uav_mobility_app.gym_envs.entities.NetworkNode import NetworkNode
from uav_mobility_app.gym_envs.enums.NetworkNodeType import NetworkNodeType
from uav_mobility_app.gym_envs.entities.Network import Network
from uav_mobility_app.gym_envs.entities.Network import ExtendedNetworkLink
from uav_mobility_app.gym_envs.utils.NetworkJSONParser import parse_json

class test_NetworkDevice(unittest.TestCase):


    def test_initialization(self):
        """Checks that the initialization of a Network is consistent.
        """
        input_path: Path = Path.cwd().joinpath("input", "network_00.json")
        input_data: dict = json.load(open(input_path))
        n_network_nodes: int = len(input_data["network_nodes"])
        n_gws = len(list(filter(
            lambda network_node: network_node["node_type"] == "GW",
            input_data["network_nodes"])))
        n_sws = len(list(filter(
            lambda network_node: network_node["node_type"] == "SW",
            input_data["network_nodes"])))
        n_aps = len(list(filter(
            lambda network_node: network_node["node_type"] == "AP",
            input_data["network_nodes"])))
        n_network_devices: int = len(input_data["network_devices"])
        n_network_links: int = len(input_data["network_links"])
        my_net = Network(input_path)
        self.assertEqual(len(my_net.nodes),
                         n_network_devices + n_network_nodes)
        self.assertEqual(len(my_net.gateways), n_gws)
        self.assertEqual(len(my_net.switches), n_sws)
        self.assertEqual(len(my_net.access_points), n_aps)
        self.assertEqual(len(my_net.edges),
                         n_network_links)

    def test_network_nodes(self):
        """Test that the network nodes are consistent w.r.t. the input
        data.
        """
        input_path: Path = Path.cwd().joinpath("input", "network_00.json")
        input_data = parse_json(input_path)
        expected_nodes: list[NetworkNode] = input_data["network_nodes"]
        my_net = Network(input_path)
        zipped_nodes = zip(my_net.network_nodes, expected_nodes)
        for (n1, n2) in zipped_nodes:
            self.assertEqual(n1.id, n2.id)
            self.assertEqual(n1.name, n2.name)
            self.assertEqual(n1.node_type, n2.node_type)
            self.assertEqual(n1.position, n2.position)

    def test_gateways(self):
        """Test that the NetworkNodes of type NetworkNodeType.GW are
        consistent w.r.t. the input data.
        """
        # TODO
        pass

    def test_switches(self):
        """Test that the NetworkNodes of type NetworkNodeType.SW are
        consistent w.r.t. the input data.
        """
        # TODO
        pass

    def test_access_points(self):
        """Test that the NetworkNodes of type NetworkNodeType.AP are
        consistent w.r.t. the input data.
        """
        # TODO
        pass

    def test_network_devices(self):
        """Test that the networkDevices are consistent w.r.t. the input
        data.
        """
        input_path: Path = Path.cwd().joinpath("input", "network_00.json")
        input_data = parse_json(input_path)
        expected_devices : list[NetworkDevice] = input_data["network_devices"]
        my_net = Network(input_path)
        zipped_devices = zip(my_net.network_devices, expected_devices)
        for (d1, d2) in zipped_devices:
            self.assertEqual(d1.id, d2.id)
            self.assertEqual(d1.name, d2.name)
            self.assertEqual(d1.device_type, d2.device_type)
            self.assertEqual(d1.throughput_req, d2.throughput_req)
            self.assertEqual(d1.delay_req, d2.delay_req)
            self.assertEqual(d1.position, d2.position)
            self.assertEqual(d1.is_active, d2.is_active)

    def test_uavs(self):
        """Test that the NetworkDevices of type NetworkDeviceType.UAV
        are consistent w.r.t. the input data.
        """
        #TODO

    def test_cams(self):
        """Test that the NetworkDevices of type NetworkDeviceType.CAM
        are consistent w.r.t. the input data.
        """
        #TODO

    def test_network_links(self):
        """Test that the NetworkLinks are consistent w.r.t. the input
        data.
        """
        input_path: Path = Path.cwd().joinpath("input", "network_00.json")
        input_data = parse_json(input_path)
        expected_links = input_data["network_links"]
        expected_links: list[NetworkLink] = [l[2] for l in expected_links]
        my_net = Network(input_path)
        zipped_links = zip(my_net.network_links, expected_links)
        for (l1, l2) in zipped_links:
            self.assertEqual(l1.id, l2.id)
            self.assertEqual(l1.name, l2.name)
            self.assertEqual(l1.max_throughput, l2.max_throughput)
            self.assertEqual(l1.available_throughput, l2.available_throughput)
            self.assertEqual(l1.routed_flows, l2.routed_flows)
            self.assertEqual(l1.delay, l2.delay)

    def test_shortest_path_to_gw(self):
        """Test that the expected shortest paths from the testing
        scenario are returned in different situations.
        """
        #TODO

    def test_assign_path_to_device(self):
        """Test that, given a path and a NetworkDevice, the resources
        that the NetworkDevice request are allocated in all the
        NetworkLinks that make up the path.
        """
        #TODO

    def test_get_path_device(self):
        """Test that given a NetworkDevice, the path were its resources
        are allocated is returned """
        #TODO

    def test_free_path_device(self):
        """Test that given a NetworkDevice, the allocation of its
        requested resources are removed from all the NetworkLinks of the
        Network.
        """
        #TODO

    def test_get_next_link(self):
        """Test that given an ExtendedNetworkLink, the list of
        ExtendedNewtorkLinks that are returned lead to the gw of the
        network.
        """
        #TODO

    def test_generate_uav_event(self):
        """Test that when an event for a NetworkDevice of type
        NetworkDeviceType.UAV is generated, the NetworkLinks are updated
        consistenly and that the NetworkDevice is set to active.
        """
        #TODO

    def test_generate_cam_event(self):
        """Test that when that events for NetworkDevices of type 
        NetworkDeviceType.CAM only inactive cameras are taken into 
        account and that the chosen is set to active.
        """