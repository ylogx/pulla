import os
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from pulla.main import app

runner = CliRunner()


@pytest.fixture
def no_git_pull():
    with patch('pulla.main.Pulla.do_pull_in') as mock_do_pull_in, \
            patch('pulla.main.Pulla.pull_all') as mock_pull_all:
        mock_do_pull_in.return_value = 0
        mock_pull_all.return_value = 0
        yield mock_do_pull_in, mock_pull_all


@patch('pulla.main.is_this_a_git_dir')
def test_should_do_pull_in_subdirectories_if_no_args(mock_is_git_dir, no_git_pull):
    mock_do_pull_in, mock_pull_all = no_git_pull
    mock_is_git_dir.return_value = False

    result = runner.invoke(app, [])

    assert result.exit_code == 0
    curdir = os.path.abspath(os.curdir)
    mock_pull_all.assert_called_once_with(curdir)


@patch('pulla.main.is_this_a_git_dir')
def test_should_do_pull_in_current_directory_if_is_git_dir(mock_is_git_dir, no_git_pull):
    mock_do_pull_in, mock_pull_all = no_git_pull
    curdir = os.path.abspath(os.curdir)
    mock_is_git_dir.return_value = True

    result = runner.invoke(app, [])

    assert result.exit_code == 0
    mock_do_pull_in.assert_called_once_with(curdir)


@patch('pulla.main.Pulla', autospec=True)
def test_should_set_verbosity_1_if_short_flag_passed(mock_pulla):
    result = runner.invoke(app, ['-v'])

    assert result.exit_code == 0
    mock_pulla.assert_called_once_with(verbosity=1, recursive=False)


@patch('pulla.main.Pulla', autospec=True)
def test_should_set_verbosity_1_if_long_flag_passed(mock_pulla):
    result = runner.invoke(app, ['--verbose'])

    assert result.exit_code == 0
    mock_pulla.assert_called_once_with(verbosity=1, recursive=False)


def test_should_fail_if_verbose_and_verbosity_both_passed():
    result = runner.invoke(app, ['-v', '-l', '2'])

    assert result.exit_code != 0


@patch('pulla.main.print_version')
def test_should_print_version_and_exit_with_short_flag(mock_print_version):
    result = runner.invoke(app, ['-V'])

    mock_print_version.assert_called_once_with()
    assert result.exit_code == 0


@patch('pulla.main.print_version')
def test_should_print_version_and_exit_with_long_flag(mock_print_version):
    result = runner.invoke(app, ['--version'])

    mock_print_version.assert_called_once_with()
    assert result.exit_code == 0
