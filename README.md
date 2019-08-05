# maillinter

A command-line line application for structuring e-mail contents.

## Command-line usage

maillinter is used via a command-line interface, ``maillinter``.

```$ maillinter --help```

Make sure that if you are using Linux you have ``xclip`` or ``xsel`` commands. Otherwise run ``sudo apt install xclip`` or ``sudo apt install xsell``. Note: ``xsel`` does not always seem to work. Otherwise on Linux, you need the gtk or PyQt4 modules installed.

Windows do not require additional modules.

On macOS, this package makes use of pbcopy and pbpaste commands, which sould come with the OS.
