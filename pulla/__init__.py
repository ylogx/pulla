from pkg_resources import get_distribution, DistributionNotFound

from .pulla import Pulla
from .logger import Logger

try:
    __version__ = get_distribution('pulla').version
except DistributionNotFound:
    __version__ = '0.0.0'
