import nltk

try:
    _ = nltk.data.load("tokenizers/punkt/english.pickle")
except LookupError:
    nltk.download("punkt", download_dir=nltk.data.path[0])

from . import base
from ._version import version as __version__
