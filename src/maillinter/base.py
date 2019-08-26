import collections
import re
import textwrap


def lint_text(text):
    """Remove consecutive whitespace characters from 'text'."""
    return " ".join(re.split(r'\s+', text, flags=re.UNICODE))


def make_subparagraphs(text):
    r"""Create a list of TextContainer instances.

    Parameters
    ==========
    text : string
        Contents of a paragraph (cannot contain \n\n)

    Returns
    =======
    list
        A list of TextContainer instances for each subparagraph in the 'text'
        that is delimited with \n character. Ordering of the TextConainter
        instances in the list reproduces 'text'.
    """
    assert '\n\n' not in text, r'cannot pass \n\n to Paragraph instance'

    subparagraphs = [TextContainer(part) for part in text.split('\n')]
    return subparagraphs


class Paragraph:
    count = 0

    def __init__(self, text):
        self._text = text
        self.subparagraphs = make_subparagraphs(text)
        self.increment_count()

    def __repr__(self):
        return f'{type(self).__name__}({self.text!r})'

    def __str__(self):
        return '\n'.join(
            subparagraph.text for subparagraph in self.subparagraphs
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
        middle_paragraphs = slice(1, len(self) - 1)
        for paragraph in self[middle_paragraphs]:
            for subparagraph in paragraph.subparagraphs:
                subparagraph._wrap(width, **kwargs)
