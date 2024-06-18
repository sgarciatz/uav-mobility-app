import unittest
import math
from uav_mobility_app.network_envs.entities.NetworkLink import NetworkLink
from uav_mobility_app.network_envs.entities.NetworkDevice import NetworkDevice
from uav_mobility_app.network_envs.enums.NetworkDeviceType import NetworkDeviceType


class test_NetworkLink(unittest.TestCase):

    def test_initialization(self):
        """Test that the NetworkLink is initialized as intended.
        """
        id = 12
        name = "link_00"
        max_throughput = 2453.1
        available_throughput = 1234.1
        routed_flows = []
        delay = 2.3
        network_link: NetworkLink = NetworkLink(id,
                                                name,
                                                max_throughput,
                                                available_throughput,
                                                routed_flows,
                                                delay)
        self.assertEqual(id, network_link.id)
        self.assertEqual(name, network_link.name)
        self.assertEqual(max_throughput, network_link.max_throughput)
        self.assertEqual(available_throughput,
                         network_link.available_throughput)
        for a, b in zip(routed_flows, network_link.routed_flows):
            self.assertEqual(a, b)
        expected_delay =\
            network_link.max_throughput - network_link.available_throughput
        expected_delay /= network_link.max_throughput
        expected_delay = (20 / math.exp(3)) * math.exp(3 * expected_delay)
        self.assertEqual(expected_delay, network_link.delay)

    def test_initialization_empty_name(self):
        """est that the NetworkLink is initialized as intended when no
        name is given.
        """
        id = 12
        max_throughput = 2453.1
        available_throughput = 1234.1
        routed_flows = []
        delay = 2.3
        network_link: NetworkLink = NetworkLink(
            link_id=id,
            max_throughput=max_throughput,
            available_throughput=available_throughput,
            routed_flows=routed_flows,
            delay=delay)
        self.assertEqual(id, network_link.id)
        self.assertEqual(str(id), network_link.name)
        self.assertEqual(max_throughput, network_link.max_throughput)
        self.assertEqual(available_throughput,
                         network_link.available_throughput)
        for a, b in zip(routed_flows, network_link.routed_flows):
            self.assertEqual(a, b)
        expected_delay =\
            network_link.max_throughput - network_link.available_throughput
        expected_delay /= network_link.max_throughput
        expected_delay = (20 / math.exp(3)) * math.exp(3 * expected_delay)
        self.assertEqual(expected_delay, network_link.delay)

    def test_change_id(self):
        """Test that the id of a NetworkDevice is not mutable."""
        id = 12
        max_throughput = 2453.1
        available_throughput = 1234.1
        routed_flows = []
        delay = 2.3
        network_link: NetworkLink = NetworkLink(
            link_id=id,
            max_throughput=max_throughput,
            available_throughput=available_throughput,
            routed_flows=routed_flows,
            delay=delay)
        exception_raised = False
        try:
            network_link.id = 123
        except:
            exception_raised = True
        finally:
            self.assertTrue(
                exception_raised,
                "Changing NetworkLink's id did not raise an exception")

    def test_change_name(self):
        """Test that the name of a NetworkLink changes as expected.
        """
        id = 12
        name = "link_00"
        max_throughput = 2453.1
        available_throughput = 1234.1
        routed_flows = []
        delay = 2.3
        network_link: NetworkLink = NetworkLink(id,
                                                name,
                                                max_throughput,
                                                available_throughput,
                                                routed_flows,
                                                delay)
        new_name = "link_11"
        network_link.link_name = new_name
        self.assertEqual(new_name, network_link.link_name)

    def test_change_max_throughput(self):
        """Test that the max_throughput of a NetworkLink is not
        mutable.
        """
        id = 12
        max_throughput = 2453.1
        available_throughput = 1234.1
        routed_flows = []
        delay = 2.3
        network_link: NetworkLink = NetworkLink(
            link_id=id,
            max_throughput=max_throughput,
            available_throughput=available_throughput,
            routed_flows=routed_flows,
            delay=delay)
        exception_raised = False
        try:
            network_link.max_throughput = 1236.1
        except:
            exception_raised = True
        finally:
            self.assertTrue(
                exception_raised,
                ("Changing NetworkLink's maximum"
                "capacity did not raise an exception"))

    def test_available_throughput(self):
        """Test that the available_throughput field changes as expected.
        Negative values nor values greater than _max_throughput are
        considered.
        """
        id = 12
        max_throughput = 2453.1
        available_throughput = 1234.1
        routed_flows = []
        delay = 2.3
        network_link: NetworkLink = NetworkLink(
            link_id=id,
            max_throughput=max_throughput,
            available_throughput=available_throughput,
            routed_flows=routed_flows,
            delay=delay)
        new_available_throughput = 2190.2
        network_link.available_throughput = new_available_throughput
        self.assertEqual(new_available_throughput,
                         network_link.available_throughput)
        available_throughput = network_link.available_throughput
        new_available_throughput = 4210.1
        network_link.available_throughput = new_available_throughput
        self.assertEqual(available_throughput,
                         network_link.available_throughput)
        new_available_throughput = -4210.1
        network_link.available_throughput = new_available_throughput
        self.assertEqual(available_throughput,
                         network_link.available_throughput)

    def test_routed_flows(self):
        """Test that the routed_flows fields works as expected. Returns
        the list which is mutable.
        """
        id = 12
        max_throughput = 2453.1
        available_throughput = 1234.1
        routed_flows = []
        delay = 2.3
        network_link: NetworkLink = NetworkLink(
            link_id=id,
            max_throughput=max_throughput,
            available_throughput=available_throughput,
            routed_flows=routed_flows,
            delay=delay)
        dev1 = NetworkDevice(device_id=1,
                             device_type=NetworkDeviceType.UAV,
                             delay_req=2.0,
                             throughput_req=1000.0,
                             position=(1,1))
        dev2 = NetworkDevice(device_id=2,
                             device_type=NetworkDeviceType.UAV,
                             delay_req=2.0,
                             throughput_req=1000.0,
                             position=(2,2))
        self.assertEqual(len(network_link.routed_flows), 0)
        network_link.routed_flows.add(dev1)
        network_link.routed_flows.add(dev2)
        self.assertEqual(len(network_link.routed_flows), 2)
        self.assertTrue(dev1 in network_link.routed_flows)
        self.assertTrue(dev2 in network_link.routed_flows)

    def test_can_route_flow(self):
        """Test that when adding flows the restrictions are respected.
        """
        id = 12
        max_throughput = 2453.1
        available_throughput = 1234.1
        routed_flows = []
        delay = 2.3
        network_link: NetworkLink = NetworkLink(
            link_id=id,
            max_throughput=max_throughput,
            available_throughput=available_throughput,
            routed_flows=routed_flows,
            delay=delay)
        dev1 = NetworkDevice(device_id=1,
                             device_type=NetworkDeviceType.UAV,
                             delay_req=2.0,
                             throughput_req=1000.0,
                             position=(1,1))
        dev2 = NetworkDevice(device_id=2,
                             device_type=NetworkDeviceType.UAV,
                             delay_req=2.0,
                             throughput_req=1500.0,
                             position=(2,2))
        self.assertTrue(network_link.can_route_flow(device=dev1))
        self.assertFalse(network_link.can_route_flow(device=dev2))

    def test_route_new_flow(self):
        """Test that when adding flows the restrictions are respected
        and that resources are allocated.
        """
        id = 12
        max_throughput = 2453.1
        available_throughput = 1234.1
        routed_flows = []
        delay = 2.3
        network_link: NetworkLink = NetworkLink(
            link_id=id,
            max_throughput=max_throughput,
            available_throughput=available_throughput,
            routed_flows=routed_flows,
            delay=delay)
        dev1 = NetworkDevice(device_id=1,
                             device_type=NetworkDeviceType.UAV,
                             delay_req=2.0,
                             throughput_req=1000.0,
                             position=(1,1))
        dev2 = NetworkDevice(device_id=2,
                             device_type=NetworkDeviceType.UAV,
                             delay_req=2.0,
                             throughput_req=1000.0,
                             position=(2,2))
        self.assertEqual(len(network_link.routed_flows), 0)
        expected_available_t = available_throughput - dev1.throughput_req
        network_link.route_new_flow(dev1)
        self.assertEqual(len(network_link.routed_flows), 1)
        self.assertAlmostEqual(expected_available_t,
                               network_link.available_throughput,
                               delta=0.01)
        result = network_link.route_new_flow(dev2)
        self.assertFalse(result)
        self.assertEqual(len(network_link.routed_flows), 1)
        self.assertAlmostEqual(expected_available_t,
                         network_link.available_throughput,
                         delta=0.01)

    def test_remove_flow(self):
        """Check that when removing flows, the list's size is
        decremented and that the throughput is freed.
        """
        id = 12
        max_throughput = 2453.1
        available_throughput = 2453.1
        routed_flows = []
        delay = 2.3
        network_link: NetworkLink = NetworkLink(
            link_id=id,
            max_throughput=max_throughput,
            available_throughput=available_throughput,
            routed_flows=routed_flows,
            delay=delay)
        dev1 = NetworkDevice(device_id=1,
                             device_type=NetworkDeviceType.UAV,
                             delay_req=2.0,
                             throughput_req=200.0,
                             position=(1,1))
        dev2 = NetworkDevice(device_id=2,
                             device_type=NetworkDeviceType.UAV,
                             delay_req=2.0,
                             throughput_req=100.0,
                             position=(2,2))
        network_link.route_new_flow(dev1)
        network_link.route_new_flow(dev2)
        expected_throughput =\
            available_throughput - dev1.throughput_req - dev2.throughput_req
        self.assertAlmostEqual(expected_throughput,
                               network_link.available_throughput,
                               delta=0.01)
        result = network_link.remove_flow(dev2)
        expected_throughput = available_throughput - dev1.throughput_req
        self.assertTrue(result)
        self.assertAlmostEqual(expected_throughput,
                               network_link.available_throughput,
                               delta=0.01)
        result = network_link.remove_flow(dev1)
        self.assertTrue(result)
        self.assertAlmostEqual(available_throughput,
                               network_link.available_throughput,
                               delta=0.01)