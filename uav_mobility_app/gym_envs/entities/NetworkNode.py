from uav_mobility_app.gym_envs.enums.NetworkNodeType import NetworkNodeType


class NetworkNode(object):


    def __init__(self,
                 node_id: int,
                 node_name: str = "",
                 node_type: NetworkNodeType = NetworkNodeType.SW,
                 position: tuple[int, int]= (0,0)) -> None:
        """The information relative to a network node

        Args:
            node_id (int): The unique identifier of the node.
            node_name (str, optional): A descriptive name of the node.
            Defaults to str(node_id).
            position (tuple[int, int], optional): The relative position
            of the node. Defaults to (0,0).
        """

        self._node_id: int = node_id
        self._node_name: str = node_name
        if (node_name == ""): self._node_name: str = str(node_id)
        self._node_type = node_type
        self._position: tuple[int,int] = position

    @property
    def id(self) -> int:
        """Get the NetworkNode's id.

        Returns:
            int: The NetworkNode's id.
        """
        return self._node_id

    @property
    def name(self) -> int:
        """Get the NetworkNode's name.

        Returns:
            int: The NetworkNode's name.
        """
        return self._node_name

    @property
    def node_type(self) -> NetworkNodeType:
        """Get the NetworkNodeType of the NetworkNode.

        Returns:
            NetworkNodeTypes: The NetworkNodeType of the NetworkNode.
        """
        return self._node_type

    @property
    def position(self) -> tuple[int, int]:
        """Returns the NetworkNode position as a tuple.

        Returns:
            tuple[int, int]: The NetworkNode position as a tuple.
        """
        return self._position

    def __str__(self) -> str:
        """Provide a descriptive string representation of the
        NetworkNode.

        Returns:
            str: The descriptive string of the NetworkNode.
        """
        str_repr = (f"Node {self._node_name} ({self._node_id})"
                    f"\n\tType: {self._node_type.name}"
                    f"\n\tPosition: {self._position}")
        return str_repr