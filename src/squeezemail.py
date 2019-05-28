import textwrap
from collections import OrderedDict

EMPTY_LINES = (
              '\n',
              '\r\n',
)
LINE_LENGHT = 65

inputfile = 'input_file.txt'
outputfile = 'squeezed_' + inputfile

with open(inputfile, 'r') as f:
    mail_read = f.readlines()

twp = textwrap.TextWrapper(width=LINE_LENGHT)

paragraph_number = 0
paragraphs = OrderedDict(
    {paragraph_number: str()}
)
for line in mail_read:
    if line in EMPTY_LINES:
        paragraph_number += 1
        paragraphs[paragraph_number] = str()
    else:
        paragraphs[paragraph_number] += line

paragraphs_wrapped = OrderedDict()
for paragraph_number, paragraph_content in paragraphs.items():
    paragraphs_wrapped[paragraph_number] = twp.wrap(paragraph_content)

with open(outputfile, 'x') as f:
    for paragraph_number, lines in paragraphs_wrapped.items():
        f.writelines('%s\n' % line for line in lines)
        f.write('\n')
