#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse

import _base


def main():
    with open(args.input, 'r') as f:
        text = f.read()
    paragraphs = text.split('\n\n')
    paragraphs = [_base.Paragraph(text) for text in paragraphs]

    mail = _base.Email(paragraphs)
    mail.wrap(args.wrap)

    if args.output:
        write(args.output, mail)
    else:
        for paragraph in mail:
            print('')
            for subparagraph in paragraph.subparagraphs:
                print(subparagraph)


def write(out_file, email_obj):
    with open(out_file, 'w') as f:
        for paragraph in email_obj:
            f.write('\n')
            for subparagraph in paragraph.subparagraphs:
                f.write(subparagraph.text)
                f.write('\n')


description_msg = 'Lint the whitespace and wrap the content of an email.'
parser = argparse.ArgumentParser(description=description_msg)
parser.add_argument('input', type=str, help='input file')
parser.add_argument('-o', dest='output', type=str, help='output file')
parser.add_argument(
    '-w', dest='wrap', type=int, default=56, help='wrapped line lenght'
)
args = parser.parse_args()


if __name__ == '__main__':
    main()
