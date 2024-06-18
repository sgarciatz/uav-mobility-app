import unittest
from uav_mobility_app.network_envs.entities.NetworkNode import NetworkNode
from uav_mobility_app.network_envs.enums.NetworkNodeType import NetworkNodeType


class test_NetworkNode(unittest.TestCase):


    def test_initialization(self):
        """Test that the NetworkNode is initialized as intended.
        """
        id = 120
        name = "node_12"
        node_type = NetworkNodeType.AP
        position = (2, 2)
        network_node: NetworkNode = NetworkNode(node_id=id,
                                                node_name=name,
                                                node_type=node_type,
                                                position=position)

        self.assertEqual(id, network_node.id)
        self.assertEqual(name, network_node.name)
        self.assertEqual(node_type, network_node.node_type)
        self.assertEqual(position, network_node.position)

    def test_initialization_empty_name(self):
        """Test that the NetworkNode is initialized as intended when
        no name is given.
        """
        id = 120
        node_type = NetworkNodeType.AP
        position = (2, 2)
        network_node: NetworkNode = NetworkNode(node_id=id,
                                                node_type=node_type,
                                                position=position)
        self.assertEqual(id, network_node.id)
        self.assertEqual(str(id), network_node.name)
        self.assertEqual(node_type, network_node.node_type)
        self.assertEqual(position, network_node.position)

    def test_change_id(self):
        """Test that the id of a NetworkNode is not mutable."""
        id = 120
        node_type = NetworkNodeType.AP
        position = (2, 2)
        network_node: NetworkNode = NetworkNode(node_id=id,
                                                node_type=node_type,
                                                position=position)
        exception_raised = False
        try:
            network_node.id = 123
        except:
            exception_raised = True
        finally:
            self.assertTrue(
                exception_raised,
                "Changing NetworkNode's id did not raise an exception")

    def test_change_name(self):
        """Test that the name of a NetworkNode is not mutable."""
        id = 120
        name = "node_12"
        node_type = NetworkNodeType.AP
        position = (2, 2)
        network_node: NetworkNode = NetworkNode(node_id=id,
                                                node_name=name,
                                                node_type=node_type,
                                                position=position)
        exception_raised = False
        try:
            network_node.name = "node_1121"
        except:
            exception_raised = True
        finally:
            self.assertTrue(
                exception_raised,
                "Changing NetworkNode's name did not raise an exception")

    def test_change_node_type(self):
        """Test that the node_type of a NetworkNode is not mutable."""
        id = 120
        name = "node_12"
        node_type = NetworkNodeType.AP
        position = (2, 2)
        network_node: NetworkNode = NetworkNode(node_id=id,
                                                node_name=name,
                                                node_type=node_type,
                                                position=position)
        exception_raised = False
        try:
            network_node.node_type = NetworkNodeType.GW
        except:
            exception_raised = True
        finally:
            self.assertTrue(
                exception_raised,
                "Changing NetworkNode's node_type did not raise an exception")

    def test_change_position(self):
        """Test that the position of a NetworkNode is not mutable."""
        id = 120
        name = "node_12"
        node_type = NetworkNodeType.AP
        position = (2, 2)
        network_node: NetworkNode = NetworkNode(node_id=id,
                                                node_name=name,
                                                node_type=node_type,
                                                position=position)
        exception_raised = False
        try:
            network_node.position = (1,1)
        except:
            exception_raised = True
        finally:
            self.assertTrue(
                exception_raised,
                "Changing NetworkNode's position did not raise an exception")