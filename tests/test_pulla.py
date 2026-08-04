import os
from itertools import chain
from unittest.mock import call, patch

import pytest

from pulla import Pulla

DIRECTORIES_FOLDER = ('a', 'b', 'c')
DIRECTORY_SUB_FOLDER = ('d', 'e', 'f')


def calls_for_process_creation(directories_to_be_pulled, puller):
    """
    :return: list with format
    [
        call(args=['dir1'], target=puller.do_pull_in),
        call().start(),
        call(args=['dir2'], target=puller.do_pull_in),
        call().start(),
    ]
    """
    return list(chain.from_iterable(
        (
            call(args=[dir], target=puller.do_pull_in), call().start()
        ) for dir in directories_to_be_pulled))


@patch('os.walk')
@patch('pulla.pulla.is_this_a_git_dir')
@patch('multiprocessing.Process')
def test_pull_all_starts_process_for_folders_in_passed_directory_when_not_recursive(
    mock_multiprocess, mock_is_git, mock_walk
):
    mock_walk.return_value = [
        ('foo', DIRECTORIES_FOLDER, ('baz', )),
        ('foo/bar', ('d', 'e', 'f'), ('spam', 'eggs')),
    ]
    mock_is_git.return_value = True

    puller = Pulla()
    puller.pull_all('foo')

    directories_folder_to_be_pulled = [os.path.join('foo', dir) for dir in DIRECTORIES_FOLDER]
    calls = [call(dir) for dir in directories_folder_to_be_pulled]
    mock_is_git.assert_has_calls(calls)

    mock_multiprocess.assert_has_calls(
        calls_for_process_creation(directories_folder_to_be_pulled, puller))


@patch('os.walk')
@patch('pulla.pulla.is_this_a_git_dir')
@patch('multiprocessing.Process')
def test_pull_all_starts_process_for_all_folders_when_recursive(
    mock_multiprocess, mock_is_git, mock_walk
):
    mock_walk.return_value = [
        ('foo', DIRECTORIES_FOLDER, ('baz', )),
        ('foo/bar', DIRECTORY_SUB_FOLDER, ('spam', 'eggs')),
    ]
    mock_is_git.return_value = True

    puller = Pulla(recursive=True)
    puller.pull_all('foo')

    directories_to_be_pulled = (
        [os.path.join('foo', dir) for dir in DIRECTORIES_FOLDER]
        + [os.path.join('foo', 'bar', dir) for dir in DIRECTORY_SUB_FOLDER]
    )
    mock_multiprocess.assert_has_calls(
        calls_for_process_creation(directories_to_be_pulled, puller))


@pytest.fixture
def puller():
    return Pulla()


@patch('pulla.pulla.Pulla.perform_git_pull')
def test_perform_git_pull_called_for_passed_directory(mock_perform_git_pull, puller):
    puller.do_pull_in('foo')

    mock_perform_git_pull.assert_called_once_with('foo')


@patch('pulla.pulla.Pulla.perform_git_pull')
@patch('pulla.pulla.Pulla.get_formatted_status_message')
def test_status_success_when_git_command_successful(
    mock_get_formatted_status_message, mock_perform_git_pull, puller
):
    mock_perform_git_pull.return_value = 0

    puller.do_pull_in('foo')

    mock_get_formatted_status_message.assert_called_once_with('foo', 0)


@patch('pulla.pulla.Pulla.perform_git_pull')
@patch('pulla.pulla.Pulla.get_formatted_status_message')
def test_status_fail_when_git_command_successful(
    mock_get_formatted_status_message, mock_perform_git_pull, puller
):
    mock_perform_git_pull.return_value = 128

    puller.do_pull_in('foo')

    mock_get_formatted_status_message.assert_called_once_with('foo', 128)


@patch('pulla.pulla.get_git_version')
@patch('os.system')
def test_pull_done_silently_when_no_verbosity(mock_os_system_cmd, mock_git_ver, puller):
    expected_status = 128
    mock_os_system_cmd.return_value = expected_status
    mock_git_ver.return_value = '2.2.2'
    expected_cmd = 'git -C foo pull &> /dev/null'

    status = puller.perform_git_pull('foo')

    mock_os_system_cmd.assert_called_once_with(expected_cmd)
    assert status == expected_status


@patch('pulla.pulla.get_git_version')
@patch('os.system')
def test_pull_done_when_verbosity_level_set_one(mock_os_system, mock_git_ver, puller):
    puller.verbosity = 1
    mock_git_ver.return_value = '2.2.2'
    expected_cmd = 'git -C foo pull --verbose'

    puller.perform_git_pull('foo')

    mock_os_system.assert_called_once_with(expected_cmd)


def test_proper_fail_message_returned(puller):
    out = puller.get_formatted_status_message('foo', 128)
    assert out == 'foo                            [red]Fail[/red]'


def test_proper_success_message_returned(puller):
    out = puller.get_formatted_status_message('foo', 0)
    assert out == 'foo                            [green]Success[/green]'
