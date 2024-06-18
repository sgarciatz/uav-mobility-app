import json
from pathlib import Path
from network_envs.entities.NetworkNode import NetworkNode
from network_envs.entities.NetworkLink import NetworkLink
from network_envs.entities.NetworkDevice import NetworkDevice
from network_envs.enums.NetworkNodeType import NetworkNodeType
from network_envs.enums.NetworkDeviceType import NetworkDeviceType


def parse_json(file_path: Path) -> dict:
    """Given a file path, creates a dict with all the NetworkDevices,
    NetworkNodes and NetworkLinks.

    Args:
        file_pah (Path): The path of the file to parse.

    Returns:
        dict: The dict with all the NetworkDevices, NetworkNodes and
        NetworkLinks.
    """
    with open(file_path) as file_path:
        input_data = json.load(file_path)
    network_nodes: list[NetworkNode] = []
    for nd in input_data["network_nodes"]:
        network_node = NetworkNode(nd["node_id"],
                                   nd["name"],
                                   NetworkNodeType[nd["node_type"]],
                                   (nd["position"][0], nd["position"][1]))
        network_nodes.append(network_node)

    network_devices: list[NetworkDevice] = []
    for nd in input_data["network_devices"]:
        network_device = NetworkDevice(nd["device_id"],
                                       nd["name"],
                                       NetworkDeviceType[nd["device_type"]],
                                       nd["delay_req"],
                                       nd["throughput_req"],
                                       (nd["position"][0], nd["position"][1]))
        network_devices.append(network_device)
    network_links: list[NetworkLink] = []
    for nd in input_data["network_links"]:
        devices: list[NetworkDevice] = []
        for device_id in nd["routed_flows"]:
            device = [d for d in network_devices if d.id == device_id][0]
            devices.append(device)
        network_link = NetworkLink(nd["link_id"],
                                   nd["name"],
                                   nd["max_throughput"],
                                   nd["available_throughput"],
                                   devices,
                                   nd["delay"])
        src_node = [n for n in network_nodes + network_devices if n.id == nd["nodes"][0]][0]
        dst_node = [n for n in network_nodes + network_devices if n.id == nd["nodes"][1]][0]
        network_links.append((src_node, dst_node, network_link))

    network_info = {
        "network_nodes": network_nodes,
        "network_links": network_links,
        "network_devices": network_devices
    }
    return network_info
