import textwrap
from functools import reduce
from operator import add, attrgetter


DEFAULT_WIDTH = 56
HARD_RETURN = '\\\\'


def hashardreturn(text):
    if HARD_RETURN in text:
        return True
    return False


def repr2text(repr_text):
    text = repr_text.replace('\n', ' ')
    text = text.rstrip()
    return text


class Paragraph:
    count = 0

    def __init__(self, repr_text):
        self.repr_text = repr_text

        if hashardreturn(self.repr_text) is True:
            parts = self.repr_text.split(HARD_RETURN)
            # TODO: Account for \t appearance. This "if" branch will
            #       strip \t and the "else" branch will not strip \t.
            self.subparagraphs = [
                SubParagraph(part.strip()) for part in parts
            ]
        else:
            self.subparagraphs = [SubParagraph(self.repr_text)]

        self.__class__.count += 1

    def __repr__(self):
        return f'Paragraph({self.repr_text!r})'

    def wrap(self, **kwargs):
        for subparagraph in self.subparagraphs:
            subparagraph.wrap(self, **kwargs)


class SubParagraph:
    count = 0

    def __init__(self, repr_text):
        self.repr_text = repr_text
        self.text = repr2text(repr_text)
        self.__class__.count += 1

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'SubParagraph({self.repr_text!r})'

    def wrap(self, width=DEFAULT_WIDTH, **kwargs):
        wrapped_lines = textwrap.wrap(self.text, width, **kwargs)
        self.text = reduce(
            add, (line if line is wrapped_lines[-1] else line + '\n'
            for line in wrapped_lines)
        )
        return None


class TextContent:

    def __init__(self, paragraphs, add_signature=False):
        self.paragraphs = paragraphs
        self.add_signature = add_signature

    def __repr__(self):
        return (
            f'TextContent({self.paragraphs!r}, '
            f'add_signature={self.add_signature!r})'
        )
