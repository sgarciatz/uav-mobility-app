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

class test_Network(unittest.TestCase):


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
        net = Network(input_path)
        self.assertEqual(len(net.nodes),
                         n_network_devices + n_network_nodes)
        self.assertEqual(len(net.gateways), n_gws)
        self.assertEqual(len(net.switches), n_sws)
        self.assertEqual(len(net.access_points), n_aps)
        self.assertEqual(len(net.edges),
                         n_network_links)

    def test_network_nodes(self):
        """Test that the network nodes are consistent w.r.t. the input
        data.
        """
        input_path: Path = Path.cwd().joinpath("input", "network_00.json")
        input_data = parse_json(input_path)
        expected_nodes: list[NetworkNode] = input_data["network_nodes"]
        net = Network(input_path)
        zipped_nodes = zip(net.network_nodes, expected_nodes)
        for (n1, n2) in zipped_nodes:
            self.assertEqual(n1.id, n2.id)
            self.assertEqual(n1.name, n2.name)
            self.assertEqual(n1.node_type, n2.node_type)
            self.assertEqual(n1.position, n2.position)

    def test_gateways(self):
        """Test that the NetworkNodes of type NetworkNodeType.GW are
        consistent w.r.t. the input data.
        """
        input_path: Path = Path.cwd().joinpath("input", "network_00.json")
        input_data: list[NetworkNode] = parse_json(input_path)["network_nodes"]
        expected_gateways: list[NetworkNode] = list(filter(
            lambda network_node: network_node.node_type == "GW",
            input_data))
        net = Network(input_path)
        zipped_gateways = zip(net.gateways, expected_gateways)
        for (g1, g2) in zipped_gateways:
            self.assertEqual(g1.id, g2.id)
            self.assertEqual(g1.name, g2.name)
            self.assertEqual(g1.node_type, g2.node_type)
            self.assertEqual(g1.position, g2.position)

    def test_switches(self):
        """Test that the NetworkNodes of type NetworkNodeType.SW are
        consistent w.r.t. the input data.
        """
        input_path: Path = Path.cwd().joinpath("input", "network_00.json")
        input_data: list[NetworkNode] = parse_json(input_path)["network_nodes"]
        expected_switches: list[NetworkNode] = list(filter(
            lambda network_node: network_node.node_type == "SW",
            input_data))
        net = Network(input_path)
        zipped_switches = zip(net.switches, expected_switches)
        for (s1, s2) in zipped_switches:
            self.assertEqual(s1.id, s2.id)
            self.assertEqual(s1.name, s2.name)
            self.assertEqual(s1.node_type, s2.node_type)
            self.assertEqual(s1.position, s2.position)

    def test_access_points(self):
        """Test that the NetworkNodes of type NetworkNodeType.AP are
        consistent w.r.t. the input data.
        """
        input_path: Path = Path.cwd().joinpath("input", "network_00.json")
        input_data: list[NetworkNode] = parse_json(input_path)["network_nodes"]
        expected_access_points: list[NetworkNode] = list(filter(
            lambda network_node: network_node.node_type == "AP",
            input_data))
        net = Network(input_path)
        zipped_access_points = zip(net.switches, expected_access_points)
        for (a1, a2) in zipped_access_points:
            self.assertEqual(a1.id, a2.id)
            self.assertEqual(a1.name, a2.name)
            self.assertEqual(a1.node_type, a2.node_type)
            self.assertEqual(a1.position, a2.position)

    def test_network_devices(self):
        """Test that the networkDevices are consistent w.r.t. the input
        data.
        """
        input_path: Path = Path.cwd().joinpath("input", "network_00.json")
        input_data = parse_json(input_path)
        expected_devices : list[NetworkDevice] = input_data["network_devices"]
        net = Network(input_path)
        zipped_devices = zip(net.network_devices, expected_devices)
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
        input_path: Path = Path.cwd().joinpath("input", "network_00.json")
        input_data: list[NetworkDevice] = \
            parse_json(input_path)["network_devices"]
        expected_uavs: list[NetworkDevice] = list(filter(
            lambda network_device: network_device.device_type == "UAV",
            input_data))
        net = Network(input_path)
        zipped_uavs = zip(net.uavs, expected_uavs)
        for (u1, u2) in zipped_uavs:
            self.assertEqual(u1.id, u2.id)
            self.assertEqual(u1.name, u2.name)
            self.assertEqual(u1.device_type, u2.device_type)
            self.assertEqual(u1.throughput_req, u2.throughput_req)
            self.assertEqual(u1.delay_req, u2.delay_req)
            self.assertEqual(u1.position, u2.position)
            self.assertEqual(u1.is_active, u2.is_active)

    def test_cams(self):
        """Test that the NetworkDevices of type NetworkDeviceType.CAM
        are consistent w.r.t. the input data.
        """
        input_path: Path = Path.cwd().joinpath("input", "network_00.json")
        input_data: list[NetworkDevice] = \
            parse_json(input_path)["network_devices"]
        expected_cams: list[NetworkDevice] = list(filter(
            lambda network_device: network_device.device_type == "CAM",
            input_data))
        net = Network(input_path)
        zipped_cams = zip(net.cams, expected_cams)
        for (c1, c2) in zipped_cams:
            self.assertEqual(c1.id, c2.id)
            self.assertEqual(c1.name, c2.name)
            self.assertEqual(c1.device_type, c2.device_type)
            self.assertEqual(c1.throughput_req, c2.throughput_req)
            self.assertEqual(c1.delay_req, c2.delay_req)
            self.assertEqual(c1.position, c2.position)
            self.assertEqual(c1.is_active, c2.is_active)

    def test_network_links(self):
        """Test that the NetworkLinks are consistent w.r.t. the input
        data.
        """
        input_path: Path = Path.cwd().joinpath("input", "network_00.json")
        input_data = parse_json(input_path)
        expected_links = input_data["network_links"]
        expected_links: list[NetworkLink] = [l[2] for l in expected_links]
        net = Network(input_path)
        zipped_links = zip(net.network_links, expected_links)
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
        net: Network = Network(Path.cwd().joinpath("input", "network_00.json"))

        uav0: NetworkDevice = None
        for uav in net.uavs:
            if (uav.name == "uav_00"):
                uav0 = uav
                break
        gateway: NetworkNode = None
        for gw in net.gateways:
            if (gw.name == "gateway"):
                gateway = gw
                break
        shortest_path = net.shortest_path_to_gw(network_device=uav0,
                                                gateway=gateway)

        expected_links: list[NetworkLink] = []

        ap0: NetworkNode = list(filter(lambda ap: ap.name == "ap_00",
                                  net.access_points))[0]
        expected_links.append(net[uav0][ap0]["data"])
        expected_links.append(net[ap0][uav0]["data"])
        switch_01: NetworkNode = list(filter(lambda ap: ap.name == "switch_01",
                                  net.switches))[0]
        expected_links.append(net[ap0][switch_01]["data"])
        expected_links.append(net[switch_01][ap0]["data"])
        switch_04: NetworkNode = list(filter(lambda ap: ap.name == "switch_04",
                                  net.switches))[0]
        expected_links.append(net[switch_01][switch_04]["data"])
        expected_links.append(net[switch_04][switch_01]["data"])
        expected_links.append(net[switch_04][gateway]["data"])
        expected_links.append(net[gateway][switch_04]["data"])
        zipped_links = zip(shortest_path, expected_links)
        for (l1, l2) in zipped_links:
            self.assertEqual(l1, l2)

    def test_assign_path_to_device(self):
        """Test that, given a path and a NetworkDevice, the resources
        that the NetworkDevice request are allocated in all the
        NetworkLinks that make up the path.
        """
        net: Network = Network(Path.cwd().joinpath("input", "network_00.json"))

        uav0: NetworkDevice = None
        for uav in net.uavs:
            if (uav.name == "uav_00"):
                uav0 = uav
                break
        gateway: NetworkNode = None
        for gw in net.gateways:
            if (gw.name == "gateway"):
                gateway = gw
                break
        ap0: NetworkNode = list(filter(lambda ap: ap.name == "ap_00",
                                  net.access_points))[0]
        switch_01: NetworkNode = list(filter(lambda ap: ap.name == "switch_01",
                                  net.switches))[0]
        switch_04: NetworkNode = list(filter(lambda ap: ap.name == "switch_04",
                                  net.switches))[0]
        path_of_uav0: list[NetworkLink] = []
        path_of_uav0.append(net[uav0][ap0]["data"])
        path_of_uav0.append(net[ap0][uav0]["data"])
        path_of_uav0.append(net[ap0][switch_01]["data"])
        path_of_uav0.append(net[switch_01][ap0]["data"])
        path_of_uav0.append(net[switch_01][switch_04]["data"])
        path_of_uav0.append(net[switch_04][switch_01]["data"])
        path_of_uav0.append(net[switch_04][gateway]["data"])
        path_of_uav0.append(net[gateway][switch_04]["data"])

        net.assign_path_to_device(device=uav0, path=path_of_uav0)
        for l in path_of_uav0:
            expected_available_throughput: float =\
                l.max_throughput - uav0.throughput_req
            self.assertEqual(l.available_throughput,
                             expected_available_throughput)
            self.assertTrue(uav0 in l.routed_flows)

    def test_get_path_device(self):
        """Test that given a NetworkDevice, the path were its resources
        are allocated is returned. The order of NetworksLink is irrelevant.
        """
        net: Network = Network(Path.cwd().joinpath("input", "network_00.json"))
        uav0: NetworkDevice = None
        for uav in net.uavs:
            if (uav.name == "uav_00"):
                uav0 = uav
                break
        gateway: NetworkNode = None
        for gw in net.gateways:
            if (gw.name == "gateway"):
                gateway = gw
                break
        ap0: NetworkNode = list(filter(lambda ap: ap.name == "ap_00",
                                  net.access_points))[0]
        switch_01: NetworkNode = list(filter(lambda ap: ap.name == "switch_01",
                                  net.switches))[0]
        switch_04: NetworkNode = list(filter(lambda ap: ap.name == "switch_04",
                                  net.switches))[0]
        expected_path_of_uav0: list[NetworkLink] = []
        expected_path_of_uav0.append(net[uav0][ap0]["data"])
        expected_path_of_uav0.append(net[ap0][uav0]["data"])
        expected_path_of_uav0.append(net[ap0][switch_01]["data"])
        expected_path_of_uav0.append(net[switch_01][ap0]["data"])
        expected_path_of_uav0.append(net[switch_01][switch_04]["data"])
        expected_path_of_uav0.append(net[switch_04][switch_01]["data"])
        expected_path_of_uav0.append(net[switch_04][gateway]["data"])
        expected_path_of_uav0.append(net[gateway][switch_04]["data"])
        net.assign_path_to_device(device=uav0, path=expected_path_of_uav0)
        actual_uav0_path  = net.get_path_device(uav0)
        self.assertEqual(len(expected_path_of_uav0), len(actual_uav0_path))
        for l in actual_uav0_path:
            self.assertTrue(l in expected_path_of_uav0)

    def test_free_path_device(self):
        """Test that given a NetworkDevice, the allocation of its
        requested resources are removed from all the NetworkLinks of the
        Network.
        """
        net: Network = Network(Path.cwd().joinpath("input", "network_00.json"))
        uav0: NetworkDevice = None
        for uav in net.uavs:
            if (uav.name == "uav_00"):
                uav0 = uav
                break
        gateway: NetworkNode = None
        for gw in net.gateways:
            if (gw.name == "gateway"):
                gateway = gw
                break
        ap0: NetworkNode = list(filter(lambda ap: ap.name == "ap_00",
                                  net.access_points))[0]
        switch_01: NetworkNode = list(filter(lambda ap: ap.name == "switch_01",
                                  net.switches))[0]
        switch_04: NetworkNode = list(filter(lambda ap: ap.name == "switch_04",
                                  net.switches))[0]
        path_of_uav0: list[NetworkLink] = []
        path_of_uav0.append(net[uav0][ap0]["data"])
        path_of_uav0.append(net[ap0][uav0]["data"])
        path_of_uav0.append(net[ap0][switch_01]["data"])
        path_of_uav0.append(net[switch_01][ap0]["data"])
        path_of_uav0.append(net[switch_01][switch_04]["data"])
        path_of_uav0.append(net[switch_04][switch_01]["data"])
        path_of_uav0.append(net[switch_04][gateway]["data"])
        path_of_uav0.append(net[gateway][switch_04]["data"])
        net.assign_path_to_device(device=uav0, path=path_of_uav0)

        net.free_path_device(uav0, path_of_uav0)

        for l in path_of_uav0:
            self.assertEqual(l.available_throughput, l.max_throughput)
            self.assertEqual(len(l.routed_flows), 0)

    def test_get_next_link(self):
        """Test that given an ExtendedNetworkLink, the list of
        ExtendedNewtorkLinks that are returned lead to the gw of the
        network.
        """
        net: Network = Network(Path.cwd().joinpath("input", "network_00.json"))
        ap0: NetworkNode = list(filter(lambda ap: ap.name == "ap_00",
                                  net.access_points))[0]
        switch_01: NetworkNode = list(filter(lambda ap: ap.name == "switch_01",
                                  net.switches))[0]
        switch_02: NetworkNode = list(filter(lambda ap: ap.name == "switch_02",
                                  net.switches))[0]
        switch_04: NetworkNode = list(filter(lambda ap: ap.name == "switch_04",
                                  net.switches))[0]
        current_l: NetworkLink = net[ap0][switch_01]
        l_01_02: NetworkLink = net[switch_01][switch_02]
        l_01_04: NetworkLink = net[switch_01][switch_04]

        next_links: list[ExtendedNetworkLink] = net.get_next_link((ap0,
                                                                   switch_01,
                                                                   current_l))
        self.assertEqual(len(next_links), 2)
        self.assertTrue((switch_01, switch_02, l_01_02) in next_links)
        self.assertTrue((switch_01, switch_04, l_01_04) in next_links)

    def test_generate_uav_event(self):
        """Test that when an event for a NetworkDevice of type
        NetworkDeviceType.UAV is generated, the NetworkLinks are updated
        consistenly and that the NetworkDevice is set to active.
        """
        net: Network = Network(Path.cwd().joinpath("input", "network_00.json"))
        seed: int = 0
        uav = net.generate_uav_event(seed=seed)
        self.assertTrue(uav.is_active)
        self.assertEqual(len(list(net.in_edges(uav))), 1)
        self.assertEqual(len(list(net.out_edges(uav))), 1)
        self.assertEqual(list(net.out_edges(uav))[0][1],
                         list(net.in_edges(uav))[0][0])


    def test_generate_cam_event(self):
        """Test that when that events for NetworkDevices of type
        NetworkDeviceType.CAM only inactive cameras are taken into
        account and that the chosen is set to active.
        """
        net: Network = Network(Path.cwd().joinpath("input", "network_00.json"))
        seed: int = 0
        n_cams: int = len(net.cams)
        for i in range(n_cams):
            n_inactive_cameras: int = len(list(filter(
                lambda cam: not cam.is_active,
                net.cams)))
            self.assertEqual(n_inactive_cameras, n_cams - i)
            cam = net.generate_cam_event(seed=seed)
            self.assertTrue(cam.is_active)
