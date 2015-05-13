import logging

class Logger:

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