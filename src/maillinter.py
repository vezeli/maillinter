# -*- coding: utf-8 -*-
import structure


def read_email(email_path):
    with open(email_path, 'r') as f:
        text = f.read()
    paragraphs = text.split('\n\n')
    paragraphs = [structure.Paragraph(text) for text in paragraphs]

    return structure.Email(paragraphs)

if __name__ == '__main__':
    email_file = 'input_file.txt'
    mail = read_email(email_file)
