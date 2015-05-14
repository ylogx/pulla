import sys
import logging


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
    def get_verbosity_level_from_logging_module(level):

        verbosity = logging.NOTSET

        if level == 1:
            verbosity = logging.CRITICAL
        elif level == 2:
            verbosity = logging.ERROR
        elif level == 3:
            verbosity = logging.WARNING
        elif level == 4:
            verbosity = logging.INFO
        elif level == 5:
            verbosity = logging.DEBUG

        return verbosity
