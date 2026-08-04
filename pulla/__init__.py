from importlib.metadata import version, PackageNotFoundError

from .pulla import Pulla
from .logger import Logger

try:
    __version__ = version('pulla')
except PackageNotFoundError:
    __version__ = '0.0.0'
