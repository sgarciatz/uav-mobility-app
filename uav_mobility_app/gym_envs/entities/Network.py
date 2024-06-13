import networkx as nx
from uav_mobility_app.gym_envs.utils.NetworkJSONParser import parse_json
from uav_mobility_app.gym_envs.enums.NetworkNodeType import NetworkNodeType
from uav_mobility_app.gym_envs.entities.NetworkNode import NetworkNode
from uav_mobility_app.gym_envs.entities.NetworkLink import NetworkLink
from uav_mobility_app.gym_envs.entities.NetworkDevice import NetworkDevice
from uav_mobility_app.gym_envs.enums.NetworkDeviceType import NetworkDeviceType
from uav_mobility_app.gym_envs.entities.ExtendedNetworkLink import ExtendedNetworkLink
import random

class Network(nx.DiGraph):
    """This class represents the Network as a directed graph. It is in
    charge of ensuring consistency, generating and applying events.
    """


    def __init__(self, incoming_graph_data: dict, **attr):
        """Create the network from a dictionary of NetworkNodes,
        NetworkLinks and NetworkDevices.

        Args:
            incoming_graph_data (dict): A dictionary of NetworkNodes,
            NetworkLinks and NetworkDevices.
        """
        super().__init__(None, **attr)
        network_data = parse_json(incoming_graph_data)
        self._network_nodes: list[NetworkNode] = network_data["network_nodes"]
        self._gateways: list[NetworkNode] = []
        self._switches: list[NetworkNode] = []
        self._access_points: list[NetworkNode] = []
        for n in self._network_nodes:
            if (n.node_type == NetworkNodeType.GW):
                self._gateways.append(n)
            elif (n.node_type == NetworkNodeType.SW):
                self._switches.append(n)
            elif (n.node_type == NetworkNodeType.AP):
                self._access_points.append(n)
        self._network_devices: list[NetworkDevice] =\
            network_data["network_devices"]
        self._uavs: list[NetworkDevice] = []
        self._cams: list[NetworkDevice] = []
        for d in self._network_devices:
            if (d.device_type == NetworkDeviceType.UAV):
                self._uavs.append(d)
            elif (d.device_type == NetworkDeviceType.CAM):
                self._cams.append(d)
        self._network_links: list[NetworkLink] =\
            [ d[2] for d in network_data["network_links"]]
        network_links = []
        for l in network_data["network_links"]:
            network_links.append((l[0], l[1], {"data": l[2]}))
        self.add_nodes_from(network_data["network_nodes"])
        self.add_nodes_from(network_data["network_devices"])
        self.add_edges_from(network_links)

    @property
    def network_nodes(self) -> list[NetworkNode]:
        """Returns the list of the NetworkNodes within the graph.
        ap_links.
        Returns:
            list[NetworkNode]: The list of the NetworkNodes whitin the
            graph.
        """
        return self._network_nodes

    @property
    def gateways(self) -> list[NetworkDevice]:
        """Returns the list of the NetworkDevices of type
        NetworkDeviceType.GW within the graph.

        Returns:
            list[NetworkNode]: The list of the NetworkDevices of type
        NetworkDeviceType.GW within the graph.
        """
        return self._gateways

    @property
    def switches(self) -> list[NetworkDevice]:
        """Returns the list of the NetworkDevices of type
        NetworkDeviceType.SW within the graph.

        Returns:
            list[NetworkNode]: The list of the NetworkDevices of type
        NetworkDeviceType.SW within the graph.

        """
        return self._switches

    @property
    def access_points(self) -> list[NetworkDevice]:
        """Returns the list of the NetworkDevices of type
        NetworkDeviceType.AP within the graph.

        Returns:
            list[NetworkNode]: The list of the NetworkDevices of type
        NetworkDeviceType.AP within the graph.
        """
        return self._access_points

    @property
    def network_devices(self) -> list[NetworkDevice]:
        """Returns the list of the NetworkDevices within the graph.

        Returns:
            list[NetworkNode]: The list of the NetworkDevices whitin the
            graph.
        """
        return self._network_devices

    @property
    def uavs(self) -> list[NetworkDevice]:
        """Returns the list of the NetworkDevices of type
        NetworkDeviceType.UAV within the graph.

        Returns:
            list[NetworkDevice]: The list of the NetworkDevices of type
            NetworkDeviceType.UAV within the graph.
        """
        return self._uavs

    @property
    def cams(self) -> list[NetworkDevice]:
        """Returns the list of the NetworkDevices of type
        NetworkDeviceType.CAM within the graph.

        Returns:
            list[NetworkDevice]: The list of the NetworkDevices of type
            NetworkDeviceType.CAM within the graph.
        """
        return self._cams

    @property
    def network_links(self) -> list[NetworkLink]:
        """Returns the list of the NetworkLinks within the graph.

        Returns:
            list[NetworkNode]: The list of the NetworkLinks whitin the
            graph.
        """
        return self._network_links

    def shortest_path_to_gw(self,
                            network_device: NetworkDevice,
                            gateway: NetworkNode) -> list[NetworkLink]:
        """Calculates the shortest path with enough throughtput between
        the given NetworkDevice and the given Gateway.

        Args:
            network_device (NetworkDevice): The NetworkDevice from where
            the path starts.
            gateway (NetworkNode): The NetworkNode where the path ends.

        Returns:
            Any: The path
        """

        # Prune the edges that cannot provide with enough throughput
        edges_to_remove = []
        for (u,v,l) in self.edges(data=True):
            l: NetworkLink = l["data"]
            not_enough_throughput =\
                l.available_throughput < network_device.throughput_req
            is_edge_link = isinstance(u, NetworkDevice) \
                           or isinstance(v, NetworkDevice)
            if (not_enough_throughput and not is_edge_link):
                edges_to_remove.append((u,v,{"data":l}))
        self.remove_edges_from(edges_to_remove)
        # TODO Check if there is a more consistent way of doing this
        # Set the weight of edges as the NetworkLinks' delays
        for (u,v,l) in self.edges(data=True):
            l: NetworkLink = l["data"]
            self[u][v]["weight"] = l.delay
        shortest_path_nodes = nx.shortest_path(self,
                                               network_device,
                                               gateway,
                                               method="dijkstra",
                                               weight="weight")
        self.add_edges_from(edges_to_remove)
        shortest_path_pairs = zip(shortest_path_nodes[0:-1],
                                   shortest_path_nodes[1:])
        links = []
        for u, v in shortest_path_pairs:
            links.append(self.get_edge_data(u, v)["data"])
            links.append(self.get_edge_data(v, u)["data"])

        return links

    def assign_path_to_device(self,
                              device: NetworkDevice,
                              path: list[NetworkLink]) -> bool:
        """Given a path and a NetworkDevice, tries to allocate the
        resources for the NetworkDevice's worflow in all NetworkLinks.

        Args:
            network_device (NetworkDevice): The NetworkDevice whose
            workflow is going to be selected.
            path (list[NetworkLink]): The sequence of NetworkLinks
            through which the NetworkDevice's workflows is going to be
            routed.

        Returns:
            bool: Whether the path could be allocated.
        """
        # pruned_path: list[NetworkLink] = []
        # for (u,v,l) in self.edges(data=True):
        #     l: NetworkLink = l["data"]
        #     is_edge_link = isinstance(u, NetworkDevice) \
        #                    or isinstance(v, NetworkDevice)
        #     if (not is_edge_link and l in path):
        #         pruned_path.append(l)
        for l in path:
            if (not l.can_route_flow(device)):
                return False
        for l in path:
            l.route_new_flow(device)
        return True

    def get_path_device(self, device: NetworkDevice) -> list[NetworkLink]:
        """Returns the path through which the NetworkDevice workflow is
        routed.

        Args:
            device (NetworkDevice): The NetworkDevice whose path is
            requested.

        Returns:
            list[NetworkLink]: The list of NetworkLinks through
            which the traffic is routed.
        """
        links = []
        for link in self._network_links:
            if (device in link.routed_flows):
                links.append(link)
        return links

    def free_path_device(self,
                         device: NetworkDevice,
                         path: list[NetworkLink]) -> None:
        """Deallocates all the resources for a NetworkDevice's workflow.

        Args:
            device (NetworkDevice): The NetworkDevice whose workflow is
            going to be deallocated from the NetworkLinks.
            path (list[NetworkLink]): The list of NetworkLinks from
            which the device's workflow is going to be deallocated.
        """
        # pruned_path: list[NetworkLink] = []
        # for (u,v,l) in self.edges(data=True):
        #     l: NetworkLink = l["data"]
        #     is_edge_link = isinstance(u, NetworkDevice) \
        #                    or isinstance(v, NetworkDevice)
        #     if (not is_edge_link and l in path):
        #         pruned_path.append(l)
        for l in path:
            l.remove_flow(device)

    def get_next_link(self,
                      link: ExtendedNetworkLink
                      ) -> list[ExtendedNetworkLink]:
        """Given a graph edge, a tuple of the src and dst NetworkNodes
        and the NetworkLink, return the next edges that lead to the
        gateway.

        Args:
            link (tuple[NetworkNode,
                        NetworkNode,
                        dict[str,NetworkDevice]]): The current
            edge.

        Returns:
            list[tuple[NetworkNode,
                       NetworkNode,
                       dict[str, NetworkLink]]]: The list of possible
            next NetworkLinks that can be selected to build the path.
        """
        dst_node: NetworkNode = link[1]
        gw: NetworkNode = self._gateways[0]

        possible_links: list[ExtendedNetworkLink] = list(self.out_edges(
            dst_node,
            data=True))
        prunned_links: list[ExtendedNetworkLink] = []
        max_path_legth: int = nx.shortest_path_length(self, dst_node, gw)
        for (u, v, l) in possible_links:
            path_length: int = nx.shortest_path_length(self, v, gw)
            if (path_length <= max_path_legth):
                prunned_links.append((u, v, l))
        return prunned_links

    def generate_uav_event(self, seed: int = None) -> NetworkDevice:
        """Generates a pseudorandom UAV related event. These kind of
        events consist on an UAV moving from one AP to another. This
        disconnection and connection process is considered to happen
        instantaneously.

        Args:
            seed (int, optional): The seed to guarantee reproducibility.
            Defaults to None.

        Returns:
            NetworkDevice: The chosen NetworkDevice.
        """

        if (seed != None):
            random.seed(seed)
        # Choose the UAV to move
        random_uav_index: int = random.randint(0, len(self._uavs) - 1)
        random_uav: NetworkDevice = self._uavs[random_uav_index]
        random_uav.is_active = True
        # Remove its current NetworkLinks
        in_link = list(self.in_edges(random_uav, data = True))[0]
        current_ap: NetworkDevice = in_link[0]
        out_link = list(self.out_edges(random_uav, data = True))[0]
        self.remove_edge(in_link[0], in_link[1])
        self.remove_edge(out_link[0], out_link[1])
        # Choose an AP to connect the UAV to
        random_ap_index: int = random.randint(0, len(self._access_points) - 2)
        aps = list(set(self._access_points) - set([current_ap]))
        random_ap: NetworkNode = aps[random_ap_index]
        # Add the new NetworkLinks
        in_network_link: NetworkLink = in_link[2]["data"]
        out_network_link: NetworkLink = out_link[2]["data"]
        in_network_link.name =\
            f"{random_ap.name} | {random_uav.name}"
        out_network_link.name =\
            f"{random_uav.name} | {random_ap.name}"
        self.add_edges_from([(random_uav,
                              random_ap,
                              {"data": in_network_link})])
        self.add_edges_from([(random_ap,
                              random_uav,
                              {"data": out_network_link})])
        return random_uav

    def generate_cam_event(self, seed: int = None) -> NetworkDevice | None:
        """Generates a pseudorandom camera related event. These kind of
        events consist on a camera starting a video streaming, thus the
        need to allocate resources for the workflow arises.

        Args:
            seed (int, optional): The seed to guarantee reproducibility.
            Defaults to None.
        Returns:
            NetworkDevice | None: _description_
        """
        # Choose a random inactive Camera to start streaming
        inactive_cams: list[NetworkDevice] = list(filter(
            lambda cam: cam.is_active == False,
            self._cams))
        random_cam_index: int = random.randint(0, len(inactive_cams)-1)
        random_cam: NetworkDevice = inactive_cams[random_cam_index]
        random_cam.is_active = True
        return random_cam

    def show_shortest_path_to_gw(self,
                                 shortest_path: list[NetworkNode]) -> None:
        """Generates a diagram that shows the NetworkLink (edges) of the
        network that connect a given NetworkDevice with a given
        NetworkNode of NetworkNodeType AP.

        Args:
            dev (NetworkDevice): The NetworkDevice whose path to gw is
            shown.
            gw (NetworkNode): The NetworkNode of type AP to which dev's
            worflow is routed.
        """
        edges = list(self.edges(data=True))
        colors = ["#000000" for _ in list(self.edges(data=True))]
        for l in shortest_path:
            for i, e in enumerate(edges):
                if (l.id == e[2]["data"].id):
                    colors[i] = "#FF0000"
        #self.remove_edges_from(edges)
        positions = {}
        labels = {}
        for n in self.nodes:
            positions[n] = [n.position[1], n.position[0]]
            labels[n] = n.name
        #colors = ["#CC00CC" for edge in list(self.edges)[::2]]
        nx.draw_networkx_nodes(self,
                               pos=positions)
        nx.draw_networkx_labels(self,
                                pos=positions,
                                labels=labels)
        edge_labels = {}
        edge_width = []
        for (u,v,l) in self.edges(data=True):
            data: NetworkLink = l["data"]
            edge_labels[(u,v)] = round(data.delay, 2)
            edge_width.append(1 + len(data.routed_flows) * 1.2)
        nx.draw_networkx_edges(
            self,
            pos=positions,
            width=edge_width,
            arrowsize=edge_width,
            edge_color=colors
        )
        nx.draw_networkx_edge_labels(
            self,
            pos=positions,
            edge_labels=edge_labels)
        plt.show()
        #self.add_edges_from(edges)

    def show_network_info(self):
        """Show the information of the network graph. For each node show
        its name and for each link, the delay that it introduces.
        """
        positions = {}
        labels = {}
        for n in self.nodes:
            positions[n] = [n.position[1], n.position[0]]
            labels[n] = n.name
        nx.draw_networkx_nodes(self,
                               pos=positions)
        nx.draw_networkx_labels(self,
                                pos=positions,
                                labels=labels)
        edge_labels = {}
        edge_width = []
        for (u,v,l) in self.edges(data=True):
            data: NetworkLink = l["data"]
            edge_labels[(u,v)] = round(data.delay, 2)
            edge_width.append(1 + len(data.routed_flows) * 1.2)
        nx.draw_networkx_edges(
            self,
            pos=positions,
            width=edge_width,
            arrowsize=edge_width,
        )
        nx.draw_networkx_edge_labels(
            self,
            pos=positions,
            edge_labels=edge_labels)



if __name__ == "__main__":
    from pathlib import Path
    import matplotlib.pyplot as plt
    my_net = Network(Path("/home/santiago/Documents/Trabajo/Workspace/uav-mobility-app/input/network_00.json"))
    nodes = [ n.id for n in my_net.nodes]
    positions = { n: [n._position[1], n._position[0]] for n in my_net.nodes}
    my_net.show_network_info()
    # nx.draw_networkx(my_net, pos=positions, with_labels=False)
    # plt.show()
    gw = my_net.gateways[0]
    # uav = my_net.uavs[0]
    # cam = my_net.cams[0]



    # shortest_path_uav = my_net.shortest_path_to_gw(uav, gw)
    # shortest_path_cam = my_net.shortest_path_to_gw(cam, gw)
    # my_net.assign_path_to_device(uav, shortest_path_uav)
    # my_net.assign_path_to_device(cam, shortest_path_cam)
    # plt.title(f"Shortest path from {uav.name} to {gw.name}")
    # my_net.show_shortest_path_to_gw(shortest_path_uav)
    # plt.title(f"Shortest path from {cam.name} to {gw.name}")
    # my_net.show_shortest_path_to_gw(shortest_path_cam)


    for _ in range(100):
        rng_uav = my_net.generate_uav_event()
        rng_uav_path = my_net.get_path_device(rng_uav)
        my_net.free_path_device(rng_uav, rng_uav_path)
        shortest_path_rng_uav = my_net.shortest_path_to_gw(rng_uav, gw)
        my_net.assign_path_to_device(rng_uav, shortest_path_rng_uav)

    for _ in range(100):
        rng_cam = my_net.generate_cam_event()
        rng_cam_path = my_net.get_path_device(rng_cam)
        my_net.free_path_device(rng_cam, rng_cam_path)
        shortest_path_rng_cam = my_net.shortest_path_to_gw(rng_cam, gw)
        my_net.assign_path_to_device(rng_cam, shortest_path_rng_cam)


    ap_00= None

    for (u, v, l) in my_net.out_edges(data=True):
        link: NetworkLink = l["data"]
        if (v.name == "ap_00"):
            ap_00 = (u, v, l)
            break
    print(my_net.get_next_link(ap_00))