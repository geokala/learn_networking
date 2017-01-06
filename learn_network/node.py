import learn_network.address_family as af

class Node(object):
    """
        A network node (host or router- though really the distinction is
        arbitrary).
    """

    def __init__(self, node_type):
        """
            Initialise this node, declaring its type.
        """
        self.node_type = node_type
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

    def add_interface(self, interface_name, address, connected_node):
        """
            Add a new interface, connecting this node to another node.
            This interface should also have an address assigned.
            Adding an existing interface will change its connected node and
            address.
        """
        self.interfaces[interface_name] = {
            'address': af.IPv4(address),
            'connected_to': connected_node,
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
