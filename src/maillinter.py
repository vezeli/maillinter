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

    for paragraph in mail:
        for subparagraph in paragraph.subparagraphs:
            print(subparagraph)
        print('')


def write(output_file, email_obj):
    with open(output_file, 'w') as f:
        for paragraph in email_obj:
            for subparagraph in paragraph.subparagraphs:
                f.write(subparagraph.text)
                f.write('\n')
            f.write('\n')


description_msg = 'Lint the whitespace and wrap the content of an email.'
parser = argparse.ArgumentParser(prog=__file__, description=description_msg)
parser.add_argument('input', type=str, help='input file')
parser.add_argument('-o', dest='output', type=str, help='output file')
parser.add_argument(
    '-w', dest='wrap', type=int, default=56, help='wrapped line lenght'
)
args = parser.parse_args()


if __name__ == '__main__':
    main()
