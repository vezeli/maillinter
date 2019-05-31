import textwrap
from functools import reduce
from operator import add


DEFAULT_WIDTH = 58

class Paragraph:

    def __init__(self, content):
        self.content = self.rstrip_whitespace(content)
        self.type = None

    def wrap(self, width=DEFAULT_WIDTH):
        """Change self.content by putting \\n at width distance."""
        raw_content = self.content.replace('\n', ' ')
        wrapped_lines = textwrap.wrap(raw_content, width)
        wrapped_lines = [line + '\n' for line in wrapped_lines]
        self.content = reduce(add, wrapped_lines)
        return None

    @staticmethod
    def rstrip_whitespace(content):
        """Remove a single/multiple whitespace character/s from the end
        of every self.content line.
        """
        while ' \n' in content or '\t\n' in content:
            content = content.replace(' \n', '\n')
            content = content.replace('\t\n', '\n')
        return content

    def __str__(self):
        return f'{self.content}'

    def __repr__(self):
        return f'Paragraph({self.content!r})'
