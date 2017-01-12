import learn_network.address_family as af
import yaml


class DuplicateNodeIdError(Exception):
    pass


class NodeNotFoundError(Exception):
    pass


class NodeManager(object):
    def __init__(self):
        self.nodes = {}

    def get_node(self, node_id):
        node = self.nodes.get(node)
        if node is None:
            raise NodeNotFoundError(node)
        return node

    def add_node(self, node_id, node_type):
        if node_id in self.nodes.keys():
            raise DuplicateNodeIdError()

        self.nodes[node_id] = Node(
            node_type=node_type,
            node_id=node_id,
        ))

    def del_node(self, node_id, node_type):
        self.nodes.pop(node_id)

    def connect_nodes(self,
                      node1_id, node1_interface, node1_address,
                      node2_id, node2_interface, node2_address):
        node1 = self.get_node(node1_id)
        node2 = self.get_node(node2_id)

        ifs1 = node1.interfaces.get(node1_interface, {})
        if ifs1.get(
            'connected_to',
            node2,
        ) not in (
            None,
            node2
        ):
            self.disconnect_interface(node1_id, node1_interface)
        ifs2 = node2.interfaces.get(node2_interface, {})
        if ifs2.get(
            'connected_to',
            node1,
        ) not in (
            None,
            node1,
        ):
            self.disconnect_interface(node2_id, node2_interface)

        node1.add_interface(
            interface_name=node1_interface,
            address=node1_address,
            remote_node=node2,
            remote_interface=node2_interface,
        )
        node2.add_interface(
            interface_name=node2_interface,
            address=node2_address,
            remote_node=node1,
            remote_interface=node1_interface,
        )

    def disconnect_interface(self, node, interface):
        node = self.get_node(node)

        interface = node.interfaces[interface]

        remote_node = interface['connected_to']['node']
        remote_interface = interface['connected_to']['interface']

        disconn = {
            'node': None,
            'interface': None,
        }

        remote_node.interfaces[remote_interface]['address'] = None
        remote_node.interfaces[remote_interface]['connected_to'] = disconn
        interface['address'] = None
        interface['connected_to'] = disconn

    def load_from_dict(self, input_dict):
        for node in input_dict['nodes']:
            self.add_node(
                node_id=node['id'],
                node_type=node['type'],
            )

        for conn in input_dict['connections']:
            details = conn.items()
(node1, {eth1: 192.0.2.1})
            node1_id = details[0][0]
            node1_if, node1_addr = details[0][1].items()
            node1_id = details[1][0]
            node1_if, node1_addr = details[1][1].items()
            self.connect_nodes(
                node1_id=node1_id,
                node1_interface=node1_if,
                node1_address=node1_addr,
                node2_id=node2_id,
                node2_interface=node2_if,
                node2_address=node2_addr,
            )

    def add_packet(self, start_node, content, start, destination):
        packet = Packet(
            content=content,
            source_address=source,
            destination_address=destination,
        )

        node = self.get_node(start_node)

        node.packets.append(packet)

    def run_network(self, iterations=10000):
        for iteration in range(iterations):
            routed_packets = []
            for node in self.nodes.values():
                routed_packets.extend(node.route_packets())
            if len(routed_packets) == 0:
                return
            for packet in routed_packets:
                packet['next_hop'].packets.append(
                    packet['packet'],
                )

    def packet_received(self, node, contents, source, destination):
        node = self.get_node(node)
        for packet in node.packets:
            if (
                packet.contents == contents
                and packet.source_address == source
                and packet.destination_address == destination
            ):
                return True
        # If we didn't find it by now, we won't.
        return False


class Node(object):
    """
        A network node (host or router- though really the distinction is
        arbitrary).
    """

    def __init__(self, node_type, node_id):
        """
            Initialise this node, declaring its type.
        """
        self.node_type = node_type
        self.id = node_id
        self.static_routes = []
        self.interfaces = {}
        self.packets = []
        self.received_packets = []
        self.unroutable_packets = []
        self.expired_packets = []

    def add_static_route(self, destination, next_hop):
        """
            Add a static route on this node.
        """
        # TODO: Later add weights
        self.static_routes.append({
            destination: next_hop,
        })

    def add_interface(self, interface_name, address, remote_node,
                      remote_interface):
        """
            Add a new interface, connecting this node to another node.
            This interface should also have an address assigned.
            Adding an existing interface will change its connected node and
            address.
        """
        self.interfaces[interface_name] = {
            'address': af.IPv4(address),
            'connected_to': {
                'node': remote_node,
                'interface': remote_interface,
            },
        }

    def route_packets(self):
        routed_packets = []
        for packet in self.packets:
            if packet.destination in self.get_addresses():
                self.received_packets.append(packet)
            next_hop = self.find_route(packet.destination)
            if packet.ttl == 0:
                self.expired_packets.append(packet)
            elif next_hop is None:
                self.unroutable_packets.append(packet)
            else:
                packet.ttl -= 1
                routed_packets.append({
                    'current': self,
                    'next_hop': next_hop,
                    'packet': packet,
                })
        return routed_packets

    def get_addresses(self):
        addresses = []
        for interface in self.interfaces.values():
            addresses.append(interface['address'].address)
        return addresses

    def find_route(self, destination):
        # Check directly connected nets first
        for interface in self.interfaces.values():
            if interface['address'].in_same_network(destination):
                return interface['connected_to']

        # Not directly connected, check route table
        # Route table should not be just static_routes
        for static_route in self.static_routes:
            route = static_route.get(destination)
            if route is not None:
                break
        return route
