import textwrap

class Paragraph:
    r"""Class that represents a paragraph of text.

    Attributes
    ==========
    spars : list
        List of tuples holding information about subparagraphs, i.e.,
        subparagraph number and subparagraph content. Subparagraphs are the
        results of splitting paragraph using the newline characters \n.
    text : string
        Holds contents of a paragraph.
    """
    def __init__(self, raw_text):
        self.spars_count = raw_text.count('\n')
        self.spars = self.make_spars(raw_text)

    @staticmethod
    def make_spars(string):
        return [(n, c) for n, c in enumerate(string.split('\n'))]

    @property
    def text(self):
        return '\n'.join(c for _, c in self.spars)

    @text.setter
    def text(self, value):
        self.spars = [(n, c) for n, c in enumerate(value.split('\n'))]

    @property
    def clean_text(self):
        ctext = str()
        for n, c in self.spars:
            if n == 0:
                ctext += " ".join(c.split())
            else:
                ctext += "\n" + " ".join(c.split())
        return ctext

    @property
    def clean_spars(self):
        return self.make_spars(self.clean_text)

    def wrap_text(self, width, **kwargs):
        wtext = str()
        for n, c in self.clean_spars:
            if n == 0:
                wtext += textwrap.fill(c, width, **kwargs)
            else:
                wtext += "\n" + textwrap.fill(c, width, **kwargs)
        return wtext

    def __repr__(self):
        return f'{type(self).__name__}({self.text!r})'

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
        return f'{type(self).__name__}({self.paragraphs!r})'

    def __str__(self):
        string = str()
        for paragraph in self:
            if paragraph is self[-1]:
                string += str(paragraph)
            else:
                string += str(paragraph) + '\n\n'
        return string

    def wrap(self, width, **kwargs):
        string = [paragraph.wrap_text(width, **kwargs) for paragraph in self]
        return '\n\n'.join(string)
