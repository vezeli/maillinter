import textwrap
from functools import reduce
from operator import add

DEFAULT_WIDTH = 58

class Paragraph:

    def __init__(self, content):
        self.content = content
        self.type = None

    def __str__(self):
        return '{}'.format(self.content)

    def __repr__(self):
        return f'Paragraph({self.content!r})'

    def wrap(self, width=DEFAULT_WIDTH):
        """Change self.content by putting \n at width distance."""
        raw_content = self.content.replace('\n', ' ')
        wrapped_lines = textwrap.wrap(raw_content, width)
        wrapped_lines = [line + '\n' for line in wrapped_lines]
        self.content = reduce(add, wrapped_lines)
