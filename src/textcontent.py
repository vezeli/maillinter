import collections
import textwrap
from functools import reduce
from operator import add, attrgetter


DEFAULT_WIDTH = 56
HARD_RETURN = '\\\\'


def hashardreturn(text):
    if HARD_RETURN in text:
        return True
    return False


Paragraph = collections.namedtuple(
    'Paragraph', ('number', 'text', 'hardreturn')
)


class TextContent:

    def __init__(self, _paragraphs, add_signature=False):
        # TODO: add control to make sure every par.hashardreturn
        #       in _paragraphs is in agreement with par.text
        paragraphs = list()
        for par in _paragraphs:
            if par.hardreturn is False:
                paragraphs.append(par)
            else:
                for extracted_par in self.restructure(par):
                    paragraphs.append(extracted_par)
        self.paragraphs = paragraphs

        self.add_signature = add_signature

    def __str__(self):
        return reduce(
            add, (par.text + '\n' for par in self.paragraphs)
        )

    def __repr__(self):
        return (
            f'TextContent({self.paragraphs!r}, '
            f'add_signature={self.add_signature!r})'
        )

    def wrap(self, width=DEFAULT_WIDTH, **kwargs)-> None:
        assert all(par.hardreturn is False for par in self.paragraphs)

        wrap_paragraphs = [
            self.wrap_paragraph(par, width, **kwargs) for par in
                                                      self.paragraphs
        ]
        self.paragraphs = [
            Paragraph(num, text, False) for num, text in
                                              enumerate(wrap_paragraphs)
        ]

        return None

    @staticmethod
    def restructure(paragraph):
        split_text = paragraph.text.split(HARD_RETURN)
        for num, text in enumerate(split_text):
            text = text[1:] if text.startswith('\n') else text
            yield Paragraph(paragraph.number + num,
                            text, hashardreturn(text))

    @staticmethod
    def wrap_paragraph(par, width=DEFAULT_WIDTH, **kwargs)-> str:
        if par.hardreturn:
            raise ParagraphNotSimple

        wrapped_lines = list()
        for wrapped_line in textwrap.wrap(par.text, width, **kwargs):
            wrapped_lines.append(wrapped_line + '\n')

        return reduce(add, wrapped_lines)


class ParagraphNotSimple(TypeError):
    pass
