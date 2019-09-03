from maillinter import __version__

try:
    from pyfiglet import figlet_format

    __sign__ = figlet_format("maillinter", font="big")
except ImportError:
    __sign__ = r"""
                 _ _ _ _       _
                (_) | (_)     | |
 _ __ ___   __ _ _| | |_ _ __ | |_ ___ _ __
| '_ ` _ \ / _` | | | | | '_ \| __/ _ \ '__|
| | | | | | (_| | | | | | | | | ||  __/ |
|_| |_| |_|\__,_|_|_|_|_|_| |_|\__\___|_|
"""

__sign__ = __sign__.rstrip() + f"\n\n{28 * ' '} v. {__version__}\n"
