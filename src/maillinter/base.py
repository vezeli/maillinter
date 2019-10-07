import collections
import itertools
import textwrap

from nltk import data

from . import form
from .parameters import DEFAULT_STYLE, DEFAULT_WRAP_LENGTH

punkt = data.load("tokenizers/punkt/english.pickle")

# Quick hack, regarding corner cases in sentence splitting,
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

    def __init__(self, content, style=DEFAULT_STYLE):
        self._spars = self._make_spars(content)
        self.style = style

    @staticmethod
    def _make_spars(string):
        return [(n, c) for n, c in enumerate(string.splitlines())]

    @property
    def text(self):
        return "\n".join(c for _, c in self._spars)

    @text.setter
    def text(self, value):
        self._spars = self._make_spars(value)

    @property
    def clean_text(self):
        cleaned_content = [" ".join(c.split()) for _, c in self._spars]
        if self._double_space_after_sentence():
            cleaned_content = ("  ".join(punkt.tokenize(cl)) for cl in cleaned_content)
        return "\n".join(cleaned_content)

    def wrap_text(self, *args, **kwargs):
        wrapped_content = [
            textwrap.fill(c, *args, **kwargs)
            for _, c in self._make_spars(self.clean_text)
        ]
        return "\n".join(wrapped_content)

    @property
    def has_links(self):
        return bool(form.RE_LINK.search(self.text))

    def _double_space_after_sentence(self):
        return {"monospaced": True, "common": False}[self.style]

    def __repr__(self):
        return f"{type(self).__name__}({self.text!r}, {self.style!r})"

    def __str__(self):
        return self.text


"""
TODO:
    MultipleParagraphs
    ==================
    Two or more Paragraphs can make MultipleParagraphs and more
    MultipleParagraphs can make more MultipleParagrpahs (__add__ method).

    superclass for Paragraphs and MultipleParagraphs
    ================================================
    So that they can inherite most of the behaviour from the super class.

    * __len__ is missing
"""


class Link(collections.UserDict):
    keys = ("anchor", "address", "reference")
    types = {
        (False, True, False): "s",
        (True, True, False): "a",
        (False, False, True): "r",
        (True, False, True): "A",
    }

    @property
    def type(self):
        return self.types[self.inspect()]

    def inspect(self):
        return tuple(bool(value) for value in self.values())

    @classmethod
    def from_iterable(cls, iterable):
        d = dict(itertools.zip_longest(cls.keys, iterable, fillvalue=None))
        try:
            del d[None]
        except KeyError:
            if None in d.values():
                raise Exception
        return cls(d)

    def __repr__(self):
        return f"{type(self).__name__}({self.data})"

    def __str__(self):
        return self.data


"""
TODO:
    manipulate data inside Link to get text which will go inside Paragraph
"""


class Email:
    def __init__(self, content):
        self.paragraphs = self.make_paragraphs(content)

    @staticmethod
    def make_paragraphs(content):
        return [Paragraph(par) for par in content.split("\n\n")]

    @property
    def text(self):
        return "\n\n".join(par.text for par in self)

    @text.setter
    def text(self, content):
        self.paragraphs = self.make_paragraphs(content)

    @property
    def links(self):
        gen_metadata = (
            form.link_metadata(match) for match in form.RE_LINK.finditer(self.text)
        )
        return [Link.from_iterable(iterable) for iterable in gen_metadata]

    def substitute_links(self):
        for num, l in enumerate(self.links, 1):
            self.text = self.text.replace(l.raw, l.as_standard_text(num))

    def wrap(self, width=DEFAULT_WRAP_LENGTH, *args, **kwargs):
        string = [par.wrap_text(width, *args, **kwargs) for par in self]
        return "\n\n".join(string)

    @classmethod
    def from_paragraphs(cls, paragraphs=None):
        if paragraphs is None:
            paragraphs = list()
        else:
            paragraphs = list(paragraphs)
        return cls("\n\n".join(par.text for par in paragraphs))

    def __len__(self):
        return len(self.paragraphs)

    def __getitem__(self, value):
        return self.paragraphs[value]

    def __repr__(self):
        return f"{type(self).__name__}({self.paragraphs!r})"

    def __str__(self):
        return self.text
