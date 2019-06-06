# -*- coding: utf-8 -*-
import collections
import textwrap
from functools import reduce
from operator import add


HARD_RETURN = '\\hardreturn'

def clean_text(repr_text):
    """Remove multiple or single whitespace except for the leading ones."""
    return ' '.join(repr_text.split())


def split_into_subparagraphs(repr_text):
    parts = repr_text.split(HARD_RETURN)
    subparagraphs = [_SubParagraph(part) for part in parts]
    return subparagraphs


class Paragraph:
    count = 0

    def __init__(self, repr_text):
        self.repr_text = repr_text
        self._subparagraphs = split_into_subparagraphs(repr_text)
        self.increment_count()

    def __str__(self):
        return '\n'.join(spar.text for spar in self._subparagraphs)

    def __repr__(self):
        return f'Paragraph({self.repr_text!r})'

    @classmethod
    def get_count(cls):
        return cls.count

    @classmethod
    def increment_count(cls):
        cls.count += 1


class _SubParagraph(Paragraph):

    def __init__(self, repr_text):
        self.repr_text = repr_text
        self.text = clean_text(repr_text)
        self.increment_count()

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'SubParagraph({self.repr_text!r})'

    def _wrap(self, width, **kwargs):
        wrapped_lines = textwrap.wrap(self.text, width, **kwargs)
        self.text = '\n'.join(line for line in wrapped_lines)


class Email(collections.UserList):

    def __init__(self, paragraphs, add_signature=False):
        self._paragraphs = paragraphs
        self.add_signature = add_signature

    def __getitem__(self, value):
        return self._paragraphs[value]

    def __repr__(self):
        return (
            f'Email({self._paragraphs!r}, '
            f'add_signature={self.add_signature!r})'
        )

    def wrap(self, width=56, **kwargs):
        for paragraph in self:
            for subparagraph in paragraph._subparagraphs:
                subparagraph._wrap(width, **kwargs)
