import textwrap

from .constants import DEFAULT_WRAP_LENGTH


class Paragraph:
    r"""Class that represents a paragraph of text.

    Parameters
    ==========
    raw_text : string
        Content of a paragraph.

    Attributes
    ==========
    spars : list
        List of tuples holding information about subparagraphs, i.e.,
        number and the content of subparagraph. Subparagraphs are the
        results of splitting paragraph using the newline characters \n.
    text : string
        Holds contents of a paragraph.
    """

    def __init__(self, raw_text):
        self.spars = self.make_spars(raw_text)

    @staticmethod
    def make_spars(string):
        return [(n, c) for n, c in enumerate(string.split("\n"))]

    @property
    def text(self):
        return "\n".join(c for _, c in self.spars)

    @text.setter
    def text(self, value):
        self.spars = [(n, c) for n, c in enumerate(value.split("\n"))]

    @property
    def clean_text(self):
        cleaned_content = [" ".join(c.split()) for _, c in self.spars]
        return "\n".join(cleaned_content)

    @property
    def clean_spars(self):
        return self.make_spars(self.clean_text)

    def wrap_text(self, **kwargs):
        w = kwargs.get("width", DEFAULT_WRAP_LENGTH)
        wrapped_content = [textwrap.fill(c, w) for _, c in self.clean_spars]
        return "\n".join(wrapped_content)

    def __repr__(self):
        return f"{type(self).__name__}({self.text!r})"

    def __str__(self):
        return self.text


class Email:
    def __init__(self, paragraphs):
        self.paragraphs = paragraphs

    def __getitem__(self, value):
        return self.paragraphs[value]

    def __len__(self):
        return len(self.paragraphs)

    def __repr__(self):
        return f"{type(self).__name__}({self.paragraphs!r})"

    def __str__(self):
        string = str()
        for paragraph in self:
            if paragraph is self[-1]:
                string += str(paragraph)
            else:
                string += str(paragraph) + "\n\n"
        return string

    def wrap(self, width, **kwargs):
        string = [paragraph.wrap_text(**kwargs) for paragraph in self]
        return "\n\n".join(string)
