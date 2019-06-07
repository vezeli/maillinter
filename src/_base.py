# -*- coding: utf-8 -*-
import collections
import textwrap
from functools import reduce
from operator import add


def clean_text(repr_text):
    """Remove ALL multiple whitespace, \\t and \\n from repr_text."""
    return ' '.join(repr_text.split())


def split_into_subparagraphs(repr_text):
    """Split Paragraph repr_text into TextContainers.

    Either \\\\ or \\newline will split the Paragraph into TextContainers."""
    repr_text = repr_text.replace('\\\\', '\\newline')
    parts = repr_text.split('\\newline')
    subparagraphs = [TextContainer(part) for part in parts]
    return subparagraphs


class Paragraph:
    count = 0

    def __init__(self, repr_text):
        self.repr_text = repr_text
        self.subparagraphs = split_into_subparagraphs(repr_text)
        self.formality = self.is_formality()
        self.increment_count()

    def is_formality(self):
        if any(subparagraph.text.istitle() for subparagraph in
                self.subparagraphs):
            return True
        else:
            return False

    def __str__(self):
        return '\n'.join(spar.text for spar in self.subparagraphs)

    def __repr__(self):
        return f'{type(self).__name__}({self.repr_text!r})'

    @classmethod
    def get_count(cls):
        return cls.count

    @classmethod
    def increment_count(cls):
        cls.count += 1


class TextContainer:

    def __init__(self, repr_text):
        self.repr_text = repr_text
        self.text = clean_text(repr_text)

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'{type(self).__name__}({self.repr_text!r})'

    def _wrap(self, width, **kwargs):
        wrapped_lines = textwrap.wrap(self.text, width, **kwargs)
        self.text = '\n'.join(line for line in wrapped_lines)


class Email:

    def __init__(self, paragraphs, add_signature=False):
        self._paragraphs = paragraphs
        self.add_signature = add_signature

    def __getitem__(self, value):
        return self._paragraphs[value]

    def __repr__(self):
        return (
            f'{type(self).__name__}({self._paragraphs!r}, '
            f'add_signature={self.add_signature!r})'
        )

    def wrap(self, width=56, **kwargs):
        for paragraph in self:
            used_kwargs = kwargs.copy()
            if paragraph.formality and kwargs.get('initial_indent') is not None:
                used_kwargs.update({'initial_indent': ''})

            for subparagraph in paragraph.subparagraphs:
                subparagraph._wrap(width, **used_kwargs)
