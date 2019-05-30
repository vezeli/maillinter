from collections import OrderedDict
from textwrap import TextWrapper


class MailContent:
    def __init__(self, inputfile):
        self.inputfile = inputfile


    def __repr__(self):
        return f'MailContent({self.inputfile!r})'


    def _get_raw_paragraphs(self):

        with open(self.inputfile, 'r') as f:
            raw_content = f.readlines()

        paragraph_number = 0
        raw_paragraphs = OrderedDict(
            {paragraph_number: str()}
        )
        for line in raw_content:
            if line in '\n':
                paragraph_number += 1
                raw_paragraphs[paragraph_number] = str()
            else:
                raw_paragraphs[paragraph_number] += line

        return raw_paragraphs


    def wrap(self, wrap_width=60):
        twp = TextWrapper(width=wrap_width)

        wrapped_paragraphs = OrderedDict()
        for number, content in self._get_raw_paragraphs().items():
            wrapped_paragraphs[number] = twp.wrap(content)

        return wrapped_paragraphs


    def write_to_file(self, outputfile=None):
        if outputfile is None:
            outputfile = 'wrapped_' + self.inputfile

        with open(outputfile, 'x') as f:
            for number, lines in self.wrap().items():
                f.writelines('%s\n' % line for line in lines)
                f.write('\n')
