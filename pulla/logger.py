import sys
import logging


LEVELS = { 'high': logging.DEBUG,
           'medium': logging.INFO,
           'low': logging.WARNING
        }

class Logger:
    def __init__(self, verbosity):
        logging_level = self.get_verbosity_level_from_logging_module(verbosity)
        log_format = logging.Formatter('%(message)s')
        stream_handle = logging.StreamHandler(sys.stdout)
        stream_handle.setFormatter(log_format)

        self.logger_handle = logging.getLogger(__name__)
        #all logs higher than the specified log_level are processed
        self.logger_handle.setLevel(logging_level)
        self.logger_handle.addHandler(stream_handle)

    def print_log(self, level, msg):
        self.logger_handle.log(level, msg)

    @staticmethod
    def get_verbosity_level_from_logging_module(verbosity):
        level = logging.NOTSET
        if verbosity == 1:
            level = logging.CRITICAL
        elif verbosity == 2:
            level = logging.ERROR
        elif verbosity == 3:
            level = logging.WARNING
        elif verbosity == 4:
            level = logging.INFO
        elif verbosity == 5:
            level = logging.DEBUG
        return level
