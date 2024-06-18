from network_envs.enums.NetworkDeviceType import NetworkDeviceType

class NetworkDevice(object):


    def __init__(self,
                 device_id: int,
                 device_name: str = "",
                 device_type: NetworkDeviceType = NetworkDeviceType.UAV,
                 delay_req: float = 10.0,
                 throughput_req: float = 100.0,
                 position: tuple[int, int] = (0, 0)) -> None:
        """The representation of a device that connects to the network.

        Args:
            device_id (int): The unique identifier of the NetworkDevice.
            device_name (str, optional): A human readable name for the
            NewtorkDevice. Defaults to str(device_id).
            device_type (NetworkDeviceType, optional): The type of the
            NetworkDevice. Defaults to NetworkDeviceType.UAV.
            delay_req (float, optional): The maximum acceptable delay
            for the traffic that this NetworkDevice generates expressed
            in ms. Defaults to 10 ms.
            throughput_req (float, optional): The needed throughput
            for the traffic that this NetworkDevice generates expressed
            in Gb/s. Defaults to 100 Gb/s.
            position (tuple[int, int], optional): The relative position
            of the node. Defaults to (0,0).
        """

        self._device_id: int = device_id
        self._device_name: str = device_name
        self._device_type: NetworkDeviceType = device_type
        if (device_name == ""): self._device_name = str(device_id)
        self._delay_req: float = delay_req
        self._throughput_req: float = throughput_req
        self._position: tuple[int, int] = position
        self._is_active: bool = False

    @property
    def id(self) -> int:
        """Get the NetworkDevice's id.

        Returns:
            int: The NetworkDevice's id.
        """
        return self._device_id

    @property
    def name(self) -> int:
        """Get the NetworkDevice's name.

        Returns:
            int: The NetworkDevice's name.
        """
        return self._device_name

    @property
    def device_type(self) -> NetworkDeviceType:
        """Returns the NetworkDevice's type.

        Returns:
            NetworkDeviceType: The NetworkDevice's type.
        """
        return self._device_type

    @property
    def throughput_req(self) -> float:
        """Returns the NetworkDevice's throughtput requirement expressed
        in Gb/s.

        Returns:
            float: the NetworkDevice's throughtput requirement expressed
        in Gb/s.
        """
        return self._throughput_req

    @property
    def delay_req(self) -> float:
        """Returns the NetworkDevice's delay requirement expressed
        in ms.

        Returns:
            float: the NetworkDevice's delay requirement expressed
        in ms.
        """
        return self._delay_req


    @property
    def position(self) -> tuple[int, int]:
        """Returns the NetworkDevice's position as a tuple.

        Returns:
            tuple[int, int]: The NetworkDevice's position as a tuple.
        """
        return self._position

    @position.setter
    def position(self, new_position: tuple[int, int]) -> bool:
        """Sets the position of the NetworkDevice to new_position iff
        it is of type NetworkDeviceType.UAV.

        Args:
            new_position (tuple[int, int]): The new position of the
            NetworkDevice.

        Returns:
            bool: Wheter the position changed or not.
        """
        if (self._device_type.value == NetworkDeviceType.CAM.value):
            return False
        self._position = new_position
        return True

    @property
    def is_active(self) -> bool:
        """Returns whether the NetworkDevice is currently active or not,
        i.e. it is sending and receiving data.

        Returns:
            bool: Whether the NetworkDevice is currently active or not
        """
        return self._is_active

    @is_active.setter
    def is_active(self, new_is_active: bool) -> None:
        """Sets the is_active of the device to new_is_active.

        Args:
            new_is_active (bool): The new value for is_active.
        """
        self._is_active = new_is_active

    def __str__(self) -> str:
        """Provide a descriptive string representation of the
        NetworkDevice.

        Returns:
            str: The descriptive string of the NetworkDevice.
        """
        str_repr = (
            f"Device {self._device_name} ({self._device_id})"
            f"\n\tIs active?: {self._is_active}"
            f"\n\tDevice type: {self._device_type.name}"
            f"\n\tRequired trhoughput: {self._throughput_req} Gb/s"
            f"\n\tMax. acceptable delay: {self._delay_req} ms"
            f"\n\tPosition: {self._position}")
        return str_repr