from enum import Enum

class NetworkNodeType(Enum):
    """A enumeration of the different types of NetworkNodes: Access
    Point (AP), Switch (SW) and Gateway(GW).
    """

    AP = 1
    SW = 2
    GW = 3