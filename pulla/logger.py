import logging

from rich.logging import RichHandler

verbosity_level = {'low': 1, 'medium': 2, 'high': 3}


class Logger:
    def __init__(self, verbosity):
        self.verbosity = verbosity
        self.logger_handle = logging.getLogger(__name__)

    def print_log(self, msg, verbosity=3):
        # logging.Logger pickles by name and is reconstructed via
        # getLogger() with no handlers, so a Logger unpickled in a
        # multiprocessing.Process child (e.g. Pulla.pull_all) needs its
        # handler and level re-attached here rather than only in __init__.
        if not self.logger_handle.handlers:
            self.logger_handle.addHandler(RichHandler(
                markup=True, show_time=False, show_level=False, show_path=False))
        self.logger_handle.setLevel(
            self.get_verbosity_level_from_logging_module(self.verbosity))

        level = self.get_verbosity_level_from_logging_module(verbosity)
        self.logger_handle.log(level, msg)

    def get_verbosity_level_from_logging_module(self, verbosity):
        level = logging.NOTSET
        if verbosity == verbosity_level['low']:
            level = logging.WARNING
        elif verbosity == verbosity_level['medium']:
            level = logging.INFO
        elif verbosity == verbosity_level['high']:
            level = logging.DEBUG
        return level
