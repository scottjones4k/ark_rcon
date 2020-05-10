"""Information about online players."""

from re import compile  # pylint: disable=W0622
from typing import NamedTuple, Tuple


__all__ = ['Players']


REGEX = compile('\\d*\. ([^,]*), \\d*')
# '\n0. azurenightwalker, 76561198056214819 \n '

class Players(NamedTuple):
    """Online players information."""

    online: int
    names: Tuple[str]

    @classmethod
    def from_response(cls, text: str):
        """Creates the players information from a server response."""
        #text = '\n0. azurenightwalker, 76561198056214819 \n '
        if text == 'No Players Connected \n ':
            return cls(0,())
        names = tuple(filter(None, map(lambda name: name.groups()[0], REGEX.finditer(text))))
        return cls(len(names), names)

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return {'online': self.online, 'names': self.names}
