import learn_network.address_family as af
import yaml


class DuplicateNodeIdError(Exception):
    pass


class NodeNotFoundError(Exception):
    pass


class NodeManager(object):
    def __init__(self):
        self.nodes = {}

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
        if node1_id not in self.nodes.keys():
            raise NodeNotFoundError(node1_id)
        if node2_id not in self.nodes.keys():
            raise NodeNotFoundError(node2_id)

        ifs1 = self.nodes[node1_id].interfaces.get(node1_interface, {})
        if ifs1.get(
            'connected_to',
            self.nodes[node2_id]
        ) not in (
            None,
            self.nodes[node2_id]
        ):
            self.disconnect_interface(node1_id, node1_interface)
        ifs2 = self.nodes[node2_id].interfaces.get(node2_interface, {})
        if ifs2.get(
            'connected_to',
            self.nodes[node1_id]
        ) not in (
            None,
            self.nodes[node1_id]
        ):
            self.disconnect_interface(node2_id, node2_interface)

        self.nodes[node1_id].add_interface(
            interface_name=node1_interface,
            address=node1_address,
            remote_node=self.nodes[node2_id],
            remote_interface=node2_interface,
        )
        self.nodes[node2_id].add_interface(
            interface_name=node2_interface,
            address=node2_address,
            remote_node=self.nodes[node1_id],
            remote_interface=node1_interface,
        )

    def disconnect_interface(self, node, interface):
        node = self.nodes.get(node)
        if node is None:
            raise NodeNotFoundError(node)

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
    '''
        There should be a list of nodes, and a method
        should be provided to add nodes, which should
        confirm that the new nodes do not have ID clashes.

expected structure:
nodes:
  - id: node1
    type: router
  - id: node2
    type: host

connections:
  - node1: eth1: 192.0.2.1
    node2: eth2: 192.0.2.2
    '''



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
        for packet in self.packets:
            if packet.destination in self.get_addresses():
                self.received_packets.append(packet)
            next_hop = self.find_route(packet.destination)
            if next_hop is None:
                self.unroutable_packets.append(packet)
            else:
                next_hop.packets.append(packet)

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
