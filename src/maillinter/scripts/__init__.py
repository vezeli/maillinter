from pkg_resources import get_distribution, DistributionNotFound

__version__ = "0.4.0"

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass

try:
    from pyfiglet import figlet_format

    __sign__  = figlet_format("maillinter", font="big")
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
