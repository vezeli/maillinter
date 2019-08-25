# -*- coding: utf-8 -*-
import collections
import re
import textwrap


def lint_text(text):
    """Remove consecutive whitespace characters from 'text'."""
    return " ".join(re.split("\s+", text, flags=re.UNICODE))


def make_subparagraphs(text):
    r"""Create TextContainer instances from 'text'.

    Parameters
    ==========
    text : string
        Contents of a paragraph (single paragraph only)

    Returns
    =======
    list
        A list of TextContainer instances for each subparagraph in the 'text'
        that is delimited with \n character. Ordering of the TextConainter
        instances in the list reproduces 'text'.
    """
    assert '\n\n' not in text, r'\n\n passed to TextContainer'

    subparagraphs = [TextContainer(part) for part in text.split('\n')]
    return subparagraphs


class Paragraph:
    count = 0

    def __init__(self, text):
        self._text = text
        self.subparagraphs = make_subparagraphs(text)
        self.soe = self.is_soe()
        self.increment_count()

    def __repr__(self):
        return f'{type(self).__name__}({self.text!r})'

    def __str__(self):
        return '\n'.join(
            subparagraph.text for subparagraph in self.subparagraphs
        )

    def is_soe(self):
        """Check if the 'Paragraph' is either a salute or an end paragraph."""
        return any(
            subparagraph.text.istitle() for subparagraph in self.subparagraphs
        )

    @property
    def text(self):
        return self._text

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

    def __init__(self, paragraphs):
        self._paragraphs = paragraphs

    def __getitem__(self, value):
        return self._paragraphs[value]

    def __len__(self):
        return len(self._paragraphs)

    def __repr__(self):
        return f'{type(self).__name__}({self._paragraphs!r})'

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

            if paragraph.soe:
                used_kwargs.update({'initial_indent': ''})

            for subparagraph in paragraph.subparagraphs:
                subparagraph._wrap(width, **used_kwargs)
