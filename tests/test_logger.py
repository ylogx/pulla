import logging
from unittest.mock import patch

import pytest

from pulla import Logger


@pytest.fixture
def logger():
    return Logger(3)


def test_should_get_critical_for_1(logger):
    assert logger.get_verbosity_level_from_logging_module(1) == logging.WARNING


def test_should_get_error_for_2(logger):
    assert logger.get_verbosity_level_from_logging_module(2) == logging.INFO


def test_should_get_warning_for_3(logger):
    assert logger.get_verbosity_level_from_logging_module(3) == logging.DEBUG


@pytest.mark.skip
@patch('pulla.logger.logging.getLogger')
def test_should_call_logger_log_with_given_params(mock_get_logger, logger):
    level = Logger.get_verbosity_level_from_logging_module(1)
    msg = 'foo bar'

    logger.print_log(level, msg)

    mock_get_logger.log.assert_called_once_with(level, msg)
