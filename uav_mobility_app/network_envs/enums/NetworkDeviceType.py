from enum import Enum

class NetworkDeviceType(Enum):
    """A enumeration of the different types of NetworkDevices: Unmanned
    Aerial Vehicle (UAV) and camera (CAM).
    """
    UAV = 1
    CAM = 2