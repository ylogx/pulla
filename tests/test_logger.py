#!/usr/bin/env python

from __future__ import print_function
import logging

try:
    import unittest
    import unittest.mock
    from unittest.mock import patch
    from unittest.mock import call
except ImportError as e:
    import unittest2 as unittest
    import mock
    from mock import patch
    from mock import call

from pulla import Logger

class TestGetVerbosityLevel(unittest.TestCase):
    def test_should_get_critical_for_1(self):
        self.assertEqual(Logger.get_verbosity_level_from_logging_module(1),
                         logging.CRITICAL)

    def test_should_get_error_for_2(self):
        self.assertEqual(Logger.get_verbosity_level_from_logging_module(2),
                         logging.ERROR)

    def test_should_get_warning_for_3(self):
        self.assertEqual(Logger.get_verbosity_level_from_logging_module(3),
                         logging.WARNING)

    def test_should_get_info_for_4(self):
        self.assertEqual(Logger.get_verbosity_level_from_logging_module(4),
                         logging.INFO)

    def test_should_get_debug_for_5(self):
        self.assertEqual(Logger.get_verbosity_level_from_logging_module(5),
                         logging.DEBUG)


class TestPrintLog(unittest.TestCase):
    def setUp(self):
        self.logger = Logger(3)

    @unittest.skip
    @patch('pulla.logger.logging.getLogger')
    def test_should_call_logger_log_with_given_params(self, mock_get_logger):
        level = Logger.get_verbosity_level_from_logging_module(1)
        msg = 'foo bar'

        self.logger.print_log(level, msg)

        mock_get_logger.log.assert_called_once_with(level, msg)


if __name__ == '__main__':
    unittest.main()
