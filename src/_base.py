# -*- coding: utf-8 -*-
import collections
import textwrap
from functools import reduce
from operator import add


NEW_LINE = r'\newline'


def lint_text(text):
    """Remove consecutive whitespace characters from 'text'."""
    return ' '.join(text.split())


def split_text(text):
    """Return 'text' as a list of strings split at '\\\\' and '\\newline'."""
    text = text.replace(r'\\', NEW_LINE)
    parts = text.split(NEW_LINE)
    subparagraphs = [TextContainer(part) for part in parts]
    return subparagraphs


class Paragraph:
    count = 0

    def __init__(self, text):
        self.text = text
        self.subparagraphs = split_text(text)
        self.salute_or_end = self.is_salute_or_end()
        self.increment_count()

    def __repr__(self):
        return f'{type(self).__name__}({self.text!r})'

    def __str__(self):
        return '\n'.join(
            subparagraph.text for subparagraph in self.subparagraphs
        )

    def is_salute_or_end(self):
        """Check if the 'Paragraph' is either a salute or an end paragraph."""
        return any(
            subparagraph.text.istitle() for subparagraph in self.subparagraphs
        )

    @classmethod
    def get_count(cls):
        return cls.count

    @classmethod
    def increment_count(cls):
        cls.count += 1


class TextContainer:

    def __init__(self, text):
        self.raw_text = text
        self.text = lint_text(text)

    def __repr__(self):
        return f'{type(self).__name__}({self.raw_text!r})'

    def __str__(self):
        return self.text

    def _wrap(self, width, **kwargs):
        wrapped_lines = textwrap.wrap(self.text, width, **kwargs)
        self.text = '\n'.join(line for line in wrapped_lines)


class Email:

    def __init__(self, paragraphs, add_signature=False):
        self._paragraphs = paragraphs
        self.add_signature = add_signature

    def __getitem__(self, value):
        return self._paragraphs[value]

    def __len__(self):
        return len(self._paragraphs)

    def __repr__(self):
        return (
            f'{type(self).__name__}({self._paragraphs!r}, '
            f'add_signature={self.add_signature!r})'
        )

    def __str__(self):
        string = str()
        for paragraph in self._paragraphs:
            if paragraph is self._paragraphs[-1]:
                string += str(paragraph)
            else:
                string += str(paragraph) + '\n\n'
        return string

    def wrap(self, width, **kwargs):
        for paragraph in self:
            used_kwargs = dict(kwargs)

            if paragraph.salute_or_end:
                used_kwargs.update({'initial_indent': ''})

            for subparagraph in paragraph.subparagraphs:
                subparagraph._wrap(width, **used_kwargs)
