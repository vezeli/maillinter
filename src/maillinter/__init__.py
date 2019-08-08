from pkg_resources import get_distribution, DistributionNotFound

__version__ = "0.4.0"

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass

