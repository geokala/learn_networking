class AddressError(Exception):
    pass


class IPv4(object):
    def __init__(self,
                 address,
                 network='255.255.255.255'):
        # We could support the lovely varied ways IPv4 addresses can be
        # represented (e.g. as integers, etc), but we don't need to yet.
        # We're also not yet dealing with addresses that aren't allowed as
        # host addresses.
        message = '
        octets = address.split('.')
        if len(octets) != 4:
            raise AddressError(
        self.address = address
        self.octets = octets
        self.network = network

    def in_same_network(self, check_address):
        
