import textwrap

class Paragraph:
    r"""Class that represents a paragraph of text.

    Parameters
    ==========
    text : str
        Holds textual content of the paragraph.
    subpars : list
        List of tuples that holds information about the subparagraphs of the
        current paragraph. Subparagraphs are the results of splitting the
        paragraph using the newline characters \n.
    """
    def __init__(self, raw_text):
        self.subpars = [
            (n, text) for n, text in enumerate(raw_text.split("\n"))
        ]
        self.num_subpars = raw_text.count("\n")

    @property
    def text(self):
        return "\n".join(text for _, text in self.subpars)

    def remove_whitespace(self):
        t = str()
        for n, text in self.subpars:
            if n == 0:
                t += " ".join(text.split())
            else:
                t += "\n" + " ".join(text.split())
        return t

    def wrap(self, width, **kwargs):
        """Wrap self.formatted_text using textwrap library."""
        try:
            wrapped_lines = textwrap.wrap(
                    self.formatted_text, width, **kwargs
            )
            self.formatted_text = '\n'.join(line for line in wrapped_lines)
        except AttributeError as e:
            print(f"Error: {e}")

    def __repr__(self):
        return f"{type(self).__name__}({self.text!r})"

    def __str__(self):
        return self.text


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
