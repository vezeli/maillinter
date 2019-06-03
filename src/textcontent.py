import textwrap
from functools import reduce
from operator import add, attrgetter


DEFAULT_WIDTH = 56
HARD_RETURN = '\\\\'


class Paragraph:
    count = 0

    def __init__(self, repr_text):
        self.repr_text = repr_text

        if self.hashardreturn(repr_text) is True:
            parts = repr_text.split(HARD_RETURN)
            self.subparagraphs = [part.strip() for part in parts]
        else:
            self.subparagraphs = [repr_text]

        self.__class__.count += 1

    def __repr__(self):
        return f'Paragraph({self.repr_text!r})'

    def wrap(self, width=DEFAULT_WIDTH, **kwargs):
        wrapped_subparagraphs = (
            textwrap.wrap(text, width, **kwargs) for text in self.subparagraphs
        )
        self.wrapped_subparagraphs = [lines for lines in wrapped_subparagraphs]
        return None

    @staticmethod
    def hashardreturn(text):
        if HARD_RETURN in text:
            return True
        return False


class TextContent:

    def __init__(self, paragraphs, add_signature=False):
        self.paragraphs = paragraphs
        self.add_signature = add_signature

    def __repr__(self):
        return (
            f'TextContent({self.paragraphs!r}, '
            f'add_signature={self.add_signature!r})'
        )

    def wrap(self, width=DEFAULT_WIDTH, **kwargs)-> None:
        _ = [
            paragraph.wrap(width, **kwargs) for paragraph in self.paragraphs
        ]
        return None
