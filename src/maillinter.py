#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import os

import _base
from _version import __version__


def main():
    with open(args.input, 'r') as f:
        text = f.read()
    paragraphs = text.split('\n\n')
    paragraphs = [_base.Paragraph(text) for text in paragraphs]

    mail = _base.Email(paragraphs)
    mail.wrap(width=args.width, initial_indent=args.indent)

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


description_msg = 'Lint and restructure e-mail text.'
parser = argparse.ArgumentParser(prog='./' + os.path.basename(__file__),
                                 description=description_msg)
parser.add_argument('input', type=str, help='input file')
parser.add_argument('-o',
                    dest='output',
                    type=str,
                    help='write program output to file')
parser.add_argument('-i',
                    dest='indent',
                    type=str,
                    default='',
                    help='add indent string to every paragraph')
parser.add_argument('-v',
                    '--version',
                    action='version',
                    version='%(prog)s {version}'.format(version=__version__))
parser.add_argument('-w',
                    dest='width',
                    type=int,
                    default=56,
                    help='set text width (default=%(default)s)')
args = parser.parse_args()

if __name__ == '__main__':
    main()
