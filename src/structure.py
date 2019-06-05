# -*- coding: utf-8 -*-
import textwrap
from functools import reduce
from operator import add


HARD_RETURN = '\\hardreturn'

def has_hard_return(text):
    return True if HARD_RETURN in text else False


def linter(repr_text):
    """Remove multiple or single whitespace except for the leading ones."""
    return ' '.join(repr_text.split())


class Paragraph:
    count = 0

    def __init__(self, repr_text):
        self.repr_text = repr_text
        self._subparagraphs = self.split_paragraph(repr_text)
        self.__class__.count += 1

    def __str__(self):
        return '\n'.join(spar.text for spar in self._subparagraphs)

    def __repr__(self):
        return f'Paragraph({self.repr_text!r})'

    @staticmethod
    def split_paragraph(repr_text):
        if has_hard_return(repr_text):
            parts = repr_text.split(HARD_RETURN)
            subparagraphs = [_SubParagraph(part.strip()) for part in parts]
        else:
            subparagraphs = [_SubParagraph(repr_text)]
        return subparagraphs


class _SubParagraph:
    count = 0

    def __init__(self, repr_text):
        self.repr_text = repr_text
        self.text = linter(repr_text)
        self.__class__.count += 1

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'SubParagraph({self.repr_text!r})'

    def _wrap(self, width, **kwargs):
        wrapped_lines = textwrap.wrap(self.text, width, **kwargs)
        self.text = '\n'.join(line for line in wrapped_lines)


class Email:

    def __init__(self, paragraphs, add_signature=False):
        self._paragraphs = paragraphs
        self.add_signature = add_signature

    def __repr__(self):
        return (
            f'Email({self._paragraphs!r}, '
            f'add_signature={self.add_signature!r})'
        )

    def wrap(self, width=56, **kwargs):
        for paragraph in self._paragraphs:
            for subparagraph in paragraph._subparagraphs:
                subparagraph._wrap(width, **kwargs)
