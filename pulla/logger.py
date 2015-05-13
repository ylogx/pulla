import sys
import logging

class Logger:

    def __init__(self, logging_level):

        log_format = logging.Formatter('%(message)s')
        stream_handle = logging.StreamHandler(sys.stdout)
        stream_handle.setFormatter(log_format)

        self.logger_handle = logging.getLogger()
        self.logger_handle.setLevel(logging_level)
        self.logger_handle.addHandler(stream_handle)

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

    def print_log(self, level, msg):

        if level == logging.CRITICAL:
            self.logger_handle.critical(msg)
        elif level == logging.ERROR:
            self.logger_handle.error(msg)
        elif level == logging.WARNING:
            self.logger_handle.warning(msg)
        elif level == logging.INFO:
            self.logger_handle.info(msg)
        elif level == logging.DEBUG:
            self.logger_handle.debug(msg)
