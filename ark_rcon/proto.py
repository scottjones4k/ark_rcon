"""Low-level protocol stuff."""

from enum import Enum
from logging import getLogger
from random import randint
from socket import SOCK_STREAM
from typing import NamedTuple
from ark_rcon.common import BaseClient
from ark_rcon.exceptions import InvalidCredentials
from ark_rcon.exceptions import InvalidPacketStructure
from ark_rcon.exceptions import RequestIdMismatch

__all__ = ['Type', 'Packet', 'Client']


LOGGER = getLogger(__file__)
TAIL = b'\0\0'


def _rand_uint32() -> int:
    """Returns a random unsigned int32."""

    return randint(0, 4_294_967_295 + 1)


class Type(Enum):
    """Available packet types."""

    LOGIN = 3
    COMMAND = 2
    RESPONSE = 0

    def __int__(self):
        """Returns the actual integer value."""
        return self.value

    def __bytes__(self):
        """Returns the integer value as little endian."""
        return int(self).to_bytes(4, 'little')


class Packet(NamedTuple):
    """An RCON packet."""

    request_id: int
    type: Type
    payload: str

    def __bytes__(self):
        """Returns the packet as bytes."""
        payload = self.request_id.to_bytes(4, 'little')
        payload += bytes(self.type)
        payload += self.payload.encode()
        payload += TAIL
        size = len(payload).to_bytes(4, 'little')
        return size + payload

    @classmethod
    def from_bytes(cls, bytes_: bytes):
        """Creates a packet from the respective bytes."""
        request_id = int.from_bytes(bytes_[:4], 'little')
        type_ = int.from_bytes(bytes_[4:8], 'little')
        payload = bytes_[8:-2]
        tail = bytes_[-2:]

        if tail != TAIL:
            raise InvalidPacketStructure('Invalid tail.', tail)

        return cls(request_id, Type(type_), payload.decode())

    @classmethod
    def from_command(cls, command: str):
        """Creates a command packet."""
        return cls(_rand_uint32(), Type.COMMAND, command)

    @classmethod
    def from_login(cls, passwd: str):
        """Creates a login packet."""
        return cls(_rand_uint32(), Type.LOGIN, passwd)


class Client(BaseClient):
    """An RCON client."""

    def __init__(self, host: str, port: int, timeout: float = None):
        """Initializes the base client with the SOCK_STREAM socket type."""
        super().__init__(SOCK_STREAM, host, port, timeout=timeout)

    def communicate(self, packet: Packet) -> Packet:
        """Sends and receives a packet."""
        self._socket.send(bytes(packet))
        header = self._socket.recv(4)
        length = int.from_bytes(header, 'little')
        payload = self._socket.recv(length)
        response = Packet.from_bytes(payload)

        if response.request_id == packet.request_id:
            return response

        raise RequestIdMismatch(packet.request_id, response.request_id)

    def login(self, passwd: str) -> bool:
        """Performs a login."""
        packet = Packet.from_login(passwd)

        try:
            self.communicate(packet)
        except RequestIdMismatch:
            raise InvalidCredentials()

        return True

    def run(self, command: str, *arguments: str, raw: bool = False) -> str:
        """Runs a command."""
        command = ' '.join((command, *arguments))
        packet = Packet.from_command(command)
        response = self.communicate(packet)
        return response if raw else response.payload
