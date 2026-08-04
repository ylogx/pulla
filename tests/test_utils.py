import os
from unittest.mock import call, patch

import pytest

from pulla.utils import is_this_a_git_dir, get_git_version


def test_is_this_a_git_dir_returns_false_for_non_git_dir():
    assert not is_this_a_git_dir('random_non_git_directory')


@patch('os.path.isdir')
def test_is_this_a_git_dir_returns_true_for_git_dir(mock_is_dir):
    test_dir = 'dummy_dir'
    possible_git_dir = os.path.join(test_dir, '.git')
    mock_is_dir.return_value = True

    output = is_this_a_git_dir(test_dir)

    mock_is_dir.assert_called_once_with(possible_git_dir)
    assert output


def test_is_this_a_git_dir_returns_false_for_null_dir():
    assert not is_this_a_git_dir(None)


GIT_VERSION_RESPONSE = 'git version 2.2.2'


@pytest.mark.skip
@patch.object(os, 'popen')
def test_correct_git_version_returned(mock_popen):
    mock_popen.return_value = GIT_VERSION_RESPONSE

    git_version = get_git_version()

    assert git_version == '2.2.2'


@patch('os.popen')
def test_opened_stream_is_closed(mock_popen):
    get_git_version()

    calls = [call('git --version'), call().read(), call().close()]
    mock_popen.assert_has_calls(calls)
