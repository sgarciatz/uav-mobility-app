import unittest
from uav_mobility_app.gym_envs.entities.NetworkDevice import NetworkDevice
from uav_mobility_app.gym_envs.enums.NetworkDeviceType import NetworkDeviceType


class test_NetworkDevice(unittest.TestCase):


    def test_initialization(self):
        """Test that the NetworkDevice is initialized as intended.
        """
        id = 120
        name = "device_00"
        dev_type = NetworkDeviceType.UAV
        delay_req = 12.1
        throughput_req = 89.3
        position = (2, 2)
        network_dev: NetworkDevice = NetworkDevice(id,
                                                   name,
                                                   dev_type,
                                                   delay_req,
                                                   throughput_req,
                                                   position)
        self.assertEqual(id, network_dev.id)
        self.assertEqual(name, network_dev.name)
        self.assertEqual(dev_type, network_dev.device_type)
        self.assertEqual(throughput_req, network_dev.throughput_req)
        self.assertEqual(delay_req, network_dev.delay_req)
        self.assertFalse(network_dev.is_active)

    def test_initialization_empty_name(self):
        """Test that the NetworkDevice is initialized as intended when
        no name is given.
        """
        id = 120
        dev_type = NetworkDeviceType.UAV
        delay_req = 12.1
        throughput_req = 89.3
        position = (2, 2)
        network_dev: NetworkDevice = NetworkDevice(
            id,
            device_type=dev_type,
            delay_req=delay_req,
            throughput_req=throughput_req,
            position=position)
        self.assertEqual(id, network_dev.id)
        self.assertEqual(str(id), network_dev.name)
        self.assertEqual(dev_type, network_dev.device_type)
        self.assertEqual(throughput_req, network_dev.throughput_req)
        self.assertEqual(delay_req, network_dev.delay_req)
        self.assertFalse(network_dev.is_active)

    def test_change_id(self):
        """Test that the id of a NetworkDevice is not mutable."""
        id = 120
        name = "device_00"
        dev_type = NetworkDeviceType.UAV
        delay_req = 12.1
        throughput_req = 89.3
        position = (2, 2)
        network_dev: NetworkDevice = NetworkDevice(id,
                                                   name,
                                                   dev_type,
                                                   delay_req,
                                                   throughput_req,
                                                   position)
        exception_raised = False
        try:
            network_dev.id = 123
        except:
            exception_raised = True
        finally:
            self.assertTrue(
                exception_raised,
                "Changing NetworkDevice's id did not raise an exception")

    def test_change_name(self):
        """Test that the name of a NetworkDevice is not mutable."""
        id = 120
        name = "device_00"
        dev_type = NetworkDeviceType.UAV
        delay_req = 12.1
        throughput_req = 89.3
        position = (2, 2)
        network_dev: NetworkDevice = NetworkDevice(id,
                                                   name,
                                                   dev_type,
                                                   delay_req,
                                                   throughput_req,
                                                   position)

        exception_raised = False
        try:
            network_dev.name = "123"
        except:
            exception_raised = True
        finally:
            self.assertTrue(
                exception_raised,
                "Changing NetworkDevice's name did not raise an exception.")

    def test_change_type(self):
        """Test that the type of a NetworkDevice is not mutable."""
        id = 120
        name = "device_00"
        dev_type = NetworkDeviceType.UAV
        delay_req = 12.1
        throughput_req = 89.3
        position = (2, 2)
        network_dev: NetworkDevice = NetworkDevice(id,
                                                   name,
                                                   dev_type,
                                                   delay_req,
                                                   throughput_req,
                                                   position)

        exception_raised = False
        try:
            network_dev.device_type = NetworkDeviceType.CAM
        except:
            exception_raised = True
        finally:
            self.assertTrue(
                exception_raised,
                "Changing NetworkDevice's type did not raise an exception.")

    def test_change_delay_req(self):
        """Test that the delay requirment of a NetworkDevice is not
        mutable.
        """
        id = 120
        name = "device_00"
        dev_type = NetworkDeviceType.UAV
        delay_req = 12.1
        throughput_req = 89.3
        position = (2, 2)
        network_dev: NetworkDevice = NetworkDevice(id,
                                                   name,
                                                   dev_type,
                                                   delay_req,
                                                   throughput_req,
                                                   position)

        exception_raised = False
        try:
            network_dev.device_type = NetworkDeviceType.CAM
        except:
            exception_raised = True
        finally:
            self.assertTrue(
                exception_raised,
                ("Changing NetworkDevice's delay"
                 "requirement did not raise an exception."))


    def test_change_througthput_req(self):
        """Test that the throughput requirment of a NetworkDevice is not
        mutable.
        """
        id = 120
        name = "device_00"
        dev_type = NetworkDeviceType.UAV
        delay_req = 12.1
        throughput_req = 89.3
        position = (2, 2)
        network_dev: NetworkDevice = NetworkDevice(id,
                                                   name,
                                                   dev_type,
                                                   delay_req,
                                                   throughput_req,
                                                   position)
        exception_raised = False
        try:
            network_dev.throughput_req = 245.6
        except:
            exception_raised = True
        finally:
            self.assertTrue(
                exception_raised,
                ("Changing NetworkDevice's throughput"
                 "requirement did not raise an exception."))

    def test_change_position_uav(self):
        """Test that the position of a NetworkDevice of type
        NetworkDeviceType.UAV changes as expected.
        """

        id = 120
        name = "device_00"
        dev_type = NetworkDeviceType.UAV
        delay_req = 12.1
        throughput_req = 89.3
        position = (2, 2)
        network_dev: NetworkDevice = NetworkDevice(id,
                                                   name,
                                                   dev_type,
                                                   delay_req,
                                                   throughput_req,
                                                   position)
        new_position = (4, 4)
        network_dev.position = new_position
        self.assertEqual(network_dev.position, new_position)

    def test_change_position_cam(self):
        """Test that the position of a NetworkDevice of type
        NetworkDeviceType.CAM does not change.
        """
        id = 120
        name = "device_00"
        dev_type = NetworkDeviceType.CAM
        delay_req = 12.1
        throughput_req = 89.3
        position = (2, 2)
        network_dev: NetworkDevice = NetworkDevice(id,
                                                   name,
                                                   dev_type,
                                                   delay_req,
                                                   throughput_req,
                                                   position)
        new_position = (4, 4)
        network_dev.position = new_position
        self.assertEqual(network_dev.position, position)

    def test_change_is_active(self):
        """Test that the is_active flag of a device can be modified to
        True and False.
        """
        id = 120
        name = "device_00"
        dev_type = NetworkDeviceType.CAM
        delay_req = 12.1
        throughput_req = 89.3
        position = (2, 2)
        network_dev: NetworkDevice = NetworkDevice(id,
                                                   name,
                                                   dev_type,
                                                   delay_req,
                                                   throughput_req,
                                                   position)
        network_dev.is_active = True
        self.assertTrue(network_dev.is_active)
        network_dev.is_active = False
        self.assertFalse(network_dev.is_active)