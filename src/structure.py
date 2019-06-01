import textwrap
import dynamic
from functools import reduce
from operator import add


DEFAULT_WIDTH = 58

def rstrip_whitespace(multilinestr):
    """Strip whitespace from the end of all lines in multiline string."""
    stripped_multilinestr = [
        line.rstrip() + '\n' for line in multilinestr.splitlines()
    ]
    return reduce(add, stripped_multilinestr)


class Paragraph:

    def __init__(self, content):
        self.content = rstrip_whitespace(content)

    def __str__(self):
        return f'{self.content}'

    def __repr__(self):
        return f'Paragraph({self.content!r})'

    def wrap(self, width=DEFAULT_WIDTH, **kwargs):
        """Wrap the string in self.contents and modify it in place.

        See textwrap.TextWrapper class for keyword args to customize the
        wrapping behaviour."""
        raw = self.content.replace('\n', ' ')
        wrapped_lines = textwrap.wrap(raw, width, **kwargs)
        wrapped_lines = [line + '\n' for line in wrapped_lines]

        self.content = reduce(add, wrapped_lines)
