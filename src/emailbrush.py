from collections import OrderedDict
from structure import Paragraph


def read_email(email_path):
    with open(email_path, 'r') as f:
        text = f.read()
    paragraphs = text.split('\n\n')

    return OrderedDict(
        {i: Paragraph(paragraph) for i, paragraph in enumerate(paragraphs)}
    )


if __name__ == '__main__':
    email_file = 'input_file.txt'
    email = read_email(email_file)
