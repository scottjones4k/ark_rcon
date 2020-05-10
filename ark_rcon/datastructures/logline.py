"""Information about log lines."""

from re import compile  # pylint: disable=W0622
from typing import NamedTuple, Tuple


__all__ = ['LogLine']


REGEX = compile('(\\d{4}\.\\d{2}\.\\d{2}_\\d{2}\.\\d{2}\.\\d{2}): (.*)\n')

class LogLine(NamedTuple):
    """Log information."""

    time: str
    log: str

    @classmethod
    def from_response(cls, text: str):
        """Creates the log lines from a server response."""
        #text = '2020.05.06_11.04.56: azurenightwalker joined this ARK!\n2020.05.06_11.06.11: azurenightwalker left this ARK!\n \n '
        if text == 'Server received, But no response!! \n ':
            return []
        return tuple(filter(None, map(lambda item: cls(item.groups()[0],item.groups()[1]), REGEX.finditer(text))))

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return {'time': self.time, 'log': self.log}
