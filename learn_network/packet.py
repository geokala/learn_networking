class Packet(object):
    """
        A network packet.
    """

    def __init__(self, content, source_address, destination_address):
        """
            Initialise this packet with content, and source and destination
            addresses.
        """
        self.content = content
        self.source_address = source_address
        self.destination_address = destination_address
        # TODO: Add address family to this
