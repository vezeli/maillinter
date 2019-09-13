import textwrap

import nltk

from .constants import DEFAULT_MONOSPACED, DEFAULT_WRAP_LENGTH

punkt = nltk.data.load("tokenizers/punkt/english.pickle")

# Quick hack, regarding corner cases in nltk-sentence splitting,
# see https://github.com/nltk/nltk/issues/2376 for details.
added_abbrev_types = {"al", "e.g", "i.e"}
for item in added_abbrev_types - punkt._params.abbrev_types:
    punkt._params.abbrev_types.add(item)


class Paragraph:
    r"""Class that represents a paragraph of text.

    Parameters
    ==========
    content : string
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

    def __init__(self, content, style="common"):
        self.spars = self.make_spars(content)
        self.style = style

    @staticmethod
    def make_spars(string):
        return [(n, c) for n, c in enumerate(string.split("\n"))]

    @property
    def text(self):
        return "\n".join(c for _, c in self.spars)

    @text.setter
    def text(self, value):
        self.spars = make_spars(value)

    @property
    def clean_text(self):
        cleaned_content = [" ".join(c.split()) for _, c in self.spars]
        if self.double_space_after_sentence:
            cleaned_content = ("  ".join(punkt.tokenize(cl)) for cl in cleaned_content)
        return "\n".join(cleaned_content)

    @property
    def clean_spars(self):
        return self.make_spars(self.clean_text)

    def wrap_text(self, **kwargs):
        w = kwargs.get("width", DEFAULT_WRAP_LENGTH)
        wrapped_content = [textwrap.fill(c, w) for _, c in self.clean_spars]
        return "\n".join(wrapped_content)

    @property
    def double_space_after_sentence(self):
        return {"monospaced": True, "common": False}[self.style]

    def __repr__(self):
        return f"{type(self).__name__}({self.text!r}, {self.style!r})"

    def __str__(self):
        return self.text


class Email:
    def __init__(self, paragraphs):
        self.paragraphs = paragraphs

    def __getitem__(self, value):
        return self.paragraphs[value]

    def __len__(self):
        return len(self.paragraphs)

    def wrap(self, width, **kwargs):
        string = [paragraph.wrap_text(**kwargs) for paragraph in self]
        return "\n\n".join(string)

    def __repr__(self):
        return f"{type(self).__name__}({self.paragraphs!r})"

    def __str__(self):
        return "\n\n".join(self)
