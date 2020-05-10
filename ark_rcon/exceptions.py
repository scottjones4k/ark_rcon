"""RCON exceptions."""


__all__ = ['InvalidPacketStructure', 'RequestIdMismatch', 'InvalidCredentials']


class InvalidPacketStructure(Exception):
    """Indicates an invalid packet structure."""


class RequestIdMismatch(Exception):
    """Indicates that the sent and received request IDs do not match."""

    def __init__(self, sent, received):
        """Sets the sent and received request IDs."""
        super().__init__(sent, received)
        self.sent = sent
        self.received = received


class InvalidCredentials(Exception):
    """Indicates invalid RCON password."""
