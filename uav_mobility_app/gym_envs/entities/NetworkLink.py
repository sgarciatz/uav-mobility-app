
from uav_mobility_app.gym_envs.entities.NetworkDevice import NetworkDevice
import math

class NetworkLink(object):


    def __init__(self,
                 link_id: int,
                 link_name: str = "",
                 max_throughput: float = 1000.0,
                 available_throughput: float = 1000.0,
                 routed_flows: list[NetworkDevice] = [],
                 delay: float = 1.0) -> None:
        """Creates a network link that connect two NetworkNodes.

        Args:
            link_id (int): The unique identifier of the link.
            link_name (str, optional): A human readable name for the
            link. Defaults to str(link_id).
            max_throughput (float, optional): The maximum throughput
            that the link can bear expressed in Gb/s. Defaults to
            1000 Gb/s.
            available_throughput (float, optional): The remaining
            throughput that the link can bear expressed in Gb/s.
            Defaults to 1000 Gb/s.
            delay (int, optional): The time delay that the channel
            introduces expressed in ms. Defaults to 1 ms.
        """
        self._link_id: int = link_id
        self._link_name: str = link_name
        if (link_name == ""): self._link_name = str(self._link_id)
        self._max_throughput: float = max_throughput
        self._available_throughput: float = available_throughput
        if (available_throughput > max_throughput):
            self._available_throughput = max_throughput
        self._routed_flows: set[NetworkDevice] = set(routed_flows)
        self._delay: float = delay

    @property
    def id(self) -> int:
        """Returns the unique identifier of the Network Link.

        Returns:
            int: The unique identifier of the Network Link.
        """
        return self._link_id

    @property
    def name(self) -> int:
        """Get the NetworkLink's name.

        Returns:
            int: The NetworkLink's name.
        """
        return self._link_name

    @name.setter
    def name(self, new_link_name: str) -> None:
        """Sets the new descriptive name for the NetworkLink.

        Args:
            new_link_name (str): The new descriptive name for the
            NetworkLink.
        """
        self._link_name = new_link_name

    @property
    def max_throughput(self) -> float:
        """Returns the maximum throughput that the NetworkLink can
        provide.

        Returns:
            float: the maximum throughput that the NetworkLink can
            provide.
        """
        return self._max_throughput

    @property
    def available_throughput(self) -> float:
        """Returns the available (remaining) throughput that the
        NetworkLink can provide.

        Returns:
            float: The available (remaining) throughput that the
        NetworkLink can provide.
        """
        return self._available_throughput

    @available_throughput.setter
    def available_throughput(self, new_available_throughput) -> bool:
        """Sets the new available throughput if it remains >= 0.

        Args:
            new_available_throughput (_type_): The new available
            throughput.

        Returns:
            bool: Whether the new available throughput could be set.
        """
        if (( new_available_throughput >= 0.0)\
            and (new_available_throughput <= self._max_throughput)):
            self._available_throughput = new_available_throughput
            return True
        else:
            return False

    @property
    def routed_flows(self) -> set[NetworkDevice]:
        """Returns the worflows of the NetworkDevices routed through
        this NetworkLink.

        Returns:
            list[NetworkDevice]: the worflows of the NetworkDevices
            routed through this NetworkLink.
        """
        return self._routed_flows

    @property
    def delay(self) -> float:
        """Returns the delay that the NetworkLink introduces.

        Returns:
            float: The delay that the NetworkLink introduces.
        """
        load = (self._max_throughput - self._available_throughput)
        load_rate = load / self._max_throughput

        return (20 / math.exp(3)) * math.exp(3 * load_rate)
        # queuing_delay =\
        #     (20 / math.exp(2.9957)) * math.exp(2.9957 * occupance_rate)
        # queuing_delay = max(0, len(self._routed_flows) - 1)

        # return self._delay + queuing_delay

    def can_route_flow(self, device: NetworkDevice) -> bool:
        """Checks whether a NetworkDevice's worflow can be routed
        through this NetworkLink.

        Args:
            device (NetworkDevice): The device whose workflow is tested.

        Returns:
            bool: Wheter if the device's workflow could be routed or
            not.
        """
        if (self._available_throughput - device.throughput_req < 0):
            return False
        if (device in self._routed_flows):
            return False
        return True

    def route_new_flow(self, device: NetworkDevice) -> bool:
        """Tries to route a new device through the NetworkLink.

        Args:
            device (NetworkDevice): The device whose workflow is going
            to be routed through the NetworkLink.

        Returns:
            bool: Wheter if the device's workflow is routed or
            not.
        """
        if (self._available_throughput - device.throughput_req < 0):
            return False
        if (device in self._routed_flows):
            return False
        self._routed_flows.add(device)
        self._available_throughput -= device.throughput_req
        return True

    def remove_flow(self, device: NetworkDevice) -> bool:
        """Tries to remove a NetworkDevice's workflow from the
        NetworkLink.

        Args:
            device (NetworkDevice): The NetworkDevice whose workflow is
            going to be removed from the NetworkLink.

        Returns:
            bool: Whether the NetworkDevice's workflow could be removed
            or not.
        """
        if (device in self._routed_flows):
            self._routed_flows.remove(device)
            self._available_throughput += device.throughput_req
            return True
        else:
            return False

    def __str__(self) -> str:
        """Provide a descriptive string representation of the
        NetworkLink.

        Returns:
            str: The descriptive string of the NetworkLink.
        """
        routed_workflows = [d.name for d in self._routed_flows]
        str_repr = (
            f"Link {self._link_name} ({self._link_id})"
            f"\n\tMax trhoughput: {self._max_throughput} Gb/s"
            f"\n\tAvailable throughput: {self._available_throughput} Gb/s"
            f"\n\tDelay: {self.delay} ms"
            f"\n\tNetworkDevices' worflows routed: {routed_workflows}")
        return str_repr
