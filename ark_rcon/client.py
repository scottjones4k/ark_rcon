"""High level client API."""

from json import dumps

from ark_rcon.datastructures import Players, LogLine
from ark_rcon.proto import Client as _Client


__all__ = ['Client']


class AdminMixin:
    """Mixin providing chat-related methods."""
    def saveworld(self):
        """Triggers a world save."""
        return self.run('saveworld')

class ChatMixin:
    """Mixin providing chat-related methods."""
    def say(self, message: str) -> str:
        """Broadcast a message to all players."""
        return self.run('broadcast', message)


class InfoMixin:
    """Server information mixin."""

    @property
    def players(self) -> Players:
        """Returns the players."""
        response = self.run('listplayers')
        return Players.from_response(response)

    def getGameLog(self):
        #'2020.05.06_11.04.56: azurenightwalker joined this ARK!\n2020.05.06_11.06.11: azurenightwalker left this ARK!\n \n '
        response = self.run('getgamelog')
        return LogLine.from_response(response)

class Client(_Client, AdminMixin, ChatMixin, InfoMixin):
    """A high-level RCON client."""
