import collections
import textwrap
from functools import reduce
from operator import add, attrgetter


DEFAULT_WIDTH = 56

Paragraph = collections.namedtuple(
    'Paragraph', ('number', 'content', 'type')
)

class TextContent:

    def __init__(self, paragraphs, add_signature=False):
        self.paragraphs = paragraphs
        self.add_signature = add_signature

    def __str__(self):
        if not isinstance(self.paragraphs, Paragraph):
            return reduce(
                add, (par.content + '\n' for par in self.paragraphs)
            )
        else:
            return self.paragraphs.content

    def __repr__(self):
        return (
            f'TextContent({self.paragraphs!r}, '
            f'add_signature={self.add_signature!r})'
        )

    def wrap(self, width=DEFAULT_WIDTH, **kwargs)-> None:
        assert all(par.type == 'simple' for par in self.paragraphs)

        wrap_paragraphs = [
            self.wrap_paragraph(par, width, **kwargs) for par in
                                                      self.paragraphs
        ]
        self.paragraphs = [
            Paragraph(num, content, 'simple') for num, content in
                                              enumerate(wrap_paragraphs)
        ]

        return None

    @staticmethod
    def wrap_paragraph(par, width=DEFAULT_WIDTH, **kwargs)-> str:
        if par.type is not 'simple':
            raise ParagraphNotSimple

        wrapped_lines = list()
        for wrapped_line in textwrap.wrap(par.content, width, **kwargs):
            wrapped_lines.append(wrapped_line + '\n')

        return reduce(add, wrapped_lines)


class ParagraphNotSimple(TypeError):
    pass
