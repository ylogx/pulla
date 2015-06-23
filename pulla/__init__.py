from pkg_resources import get_distribution

from .pulla import Pulla
from .logger import Logger

__version__ = get_distribution('pulla').version
