#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import os

import pyperclip

from maillinter import base
from maillinter.__about__ import get_local_version


def main():
    with open(args.input_file, 'r') as f:
        text = f.read()
    paragraphs = text.split('\n\n')
    paragraphs = [base.Paragraph(text) for text in paragraphs]

    mail = base.Email(paragraphs)
    mail.wrap(width=args.width, initial_indent=args.indent)

    clipboard_string = str(mail)
    pyperclip.copy(clipboard_string)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(clipboard_string)
    print(clipboard_string)

description_msg = 'Lint and restructure e-mail text.'
parser = argparse.ArgumentParser(prog='./' + os.path.basename(__file__),
                                 description=description_msg)
parser.add_argument('input_file', type=str)
parser.add_argument('-v',
                    '--version',
                    action='version',
                    version='%(prog)s {version}'.format(version=get_local_version()))
parser.add_argument('-w',
                    '--wrap',
                    dest='width',
                    metavar='width',
                    type=int,
                    default=56,
                    help='set line width (default=%(default)s)')
parser.add_argument('--indent',
                    dest='indent',
                    metavar='\'pattern\'',
                    type=str,
                    default='',
                    help='indent paragraphs with the pattern')
parser.add_argument('-S',
                    '--save',
                    dest='output',
                    metavar='FILE',
                    type=str,
                    help='save output to file')
args = parser.parse_args()

if __name__ == '__main__':
    main()
