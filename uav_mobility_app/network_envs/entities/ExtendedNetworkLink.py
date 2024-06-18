from network_envs.entities.NetworkLink import NetworkLink
from network_envs.entities.NetworkNode import NetworkNode

"""ExtendedNetworkLink is an alias to tackle the NetworkX way of dealing
with edges. It represents a pair the nodes (NetworkNodes) that compose
the edge and the data is stored in the dict. The dict only have one key:
"data" and it holds the instance of the NetworkLink object that holds
all the information of the node.
"""

ExtendedNetworkLink = tuple[NetworkNode,
                            NetworkNode,
                            dict[str, NetworkLink]]