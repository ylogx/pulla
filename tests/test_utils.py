import os
from unittest.mock import patch

from pulla.utils import is_this_a_git_dir


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
