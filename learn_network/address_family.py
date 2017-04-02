class AddressError(Exception):
    pass


class IPv4(object):
    def __init__(self,
                 address,
                 network_mask='255.255.255.255'):
        self.address = address
        self.network_mask = network_mask

    def validate_address(self, address):
        # We could support the lovely varied ways IPv4 addresses can be
        # represented (e.g. as integers, etc), but we don't need to yet.
        # We're also not yet dealing with addresses that aren't allowed as
        # host addresses.
        message = (
            'Expecting an address in the form: a.b.c.d, '
            'where a, b, c, and d are decimals between 0 and 255.'
        )
        octets = address.split('.')
        valid = True
        if len(octets) != 4:
            valid = False

        try:
            octets = [int(octet) for octet in octets]
        except ValueError:
            valid = False

        if not valid:
            raise AddressError(message)

        for octet in octets:
            if octet < 0 or octet > 255:
                raise AddressError(message)

    def in_same_network(self, check_address):
        self.validate_address(check_address)

        if check_address == self.address:
            return True

        my_addr = self._addr_to_int(self.address)
        netmask = self._addr_to_int(self.network_mask)
        compare_addr = self._addr_to_int(check_address)

        my_network = my_addr & netmask
        compare_network = compare_addr & netmask

        return my_network == compare_network

    def _addr_to_int(self, addr):
        components = addr.split('.')
        components.reverse()
        total = 0
        for i in range(0, len(components)):
            current = int(components[i]) << 8 * i
            total += current
        return total
