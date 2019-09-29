# Copyright 2019 Velibor Zeli
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os

import pyperclip

from maillinter import base
from maillinter.scripts import __version__, __sign__


def cli():
    with open(args.input_file, "r") as f:
        content = f.read()

    mail = base.Email(content)
    wrapped = mail.wrap(args.width)

    clipboard_string = wrapped
    pyperclip.copy(clipboard_string)

    if args.output:
        with open(args.output, "w") as f:
            f.write(clipboard_string)
    print(clipboard_string)


description_msg = "Lint and restructure e-mail text."
parser = argparse.ArgumentParser(
    prog="maillinter", description=description_msg
)
parser.add_argument("input_file", type=str)
parser.add_argument(
    "-v",
    "--version",
    action="version",
    version="%(prog)s {version}".format(version=__version__),
)
parser.add_argument(
    "-w",
    "--wrap",
    dest="width",
    metavar="width",
    type=int,
    default=56,
    help="set line width (default=%(default)s)",
)
parser.add_argument(
    "--indent",
    dest="indent",
    metavar="'pattern'",
    type=str,
    default="",
    help="indent paragraphs with the pattern",
)
parser.add_argument(
    "-S", "--save", dest="output", metavar="FILE", type=str, help="save output to file"
)
args = parser.parse_args()

if __name__ == "__main__":
    cli()
