# -*- coding: utf-8 -*-
import _base


def read_email(email_path):
    with open(email_path, 'r') as f:
        text = f.read()
    paragraphs = text.split('\n\n')
    paragraphs = [_base.Paragraph(text) for text in paragraphs]

    return _base.Email(paragraphs)

if __name__ == '__main__':
    email_file = 'input_file.txt'
    mail = read_email(email_file)
