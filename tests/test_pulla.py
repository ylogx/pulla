import asyncio
import os
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

from pulla import Pulla

DIRECTORIES_FOLDER = ('a', 'b', 'c')
DIRECTORY_SUB_FOLDER = ('d', 'e', 'f')


@pytest.fixture
def puller():
    return Pulla()


@patch('os.walk')
@patch('pulla.pulla.is_this_a_git_dir')
@patch('pulla.pulla.Pulla.do_pull_in')
def test_pull_all_pulls_folders_in_passed_directory_when_not_recursive(
    mock_do_pull_in, mock_is_git, mock_walk, puller
):
    mock_walk.return_value = [
        ('foo', DIRECTORIES_FOLDER, ('baz', )),
        ('foo/bar', ('d', 'e', 'f'), ('spam', 'eggs')),
    ]
    mock_is_git.return_value = True

    asyncio.run(puller.pull_all('foo'))

    directories_to_be_pulled = [os.path.join('foo', dir) for dir in DIRECTORIES_FOLDER]
    mock_is_git.assert_has_calls([call(dir) for dir in directories_to_be_pulled])
    mock_do_pull_in.assert_has_calls(
        [call(dir) for dir in directories_to_be_pulled], any_order=True)


@patch('os.walk')
@patch('pulla.pulla.is_this_a_git_dir')
@patch('pulla.pulla.Pulla.do_pull_in')
def test_pull_all_pulls_all_folders_when_recursive(mock_do_pull_in, mock_is_git, mock_walk):
    mock_walk.return_value = [
        ('foo', DIRECTORIES_FOLDER, ('baz', )),
        ('foo/bar', DIRECTORY_SUB_FOLDER, ('spam', 'eggs')),
    ]
    mock_is_git.return_value = True

    puller = Pulla(recursive=True)
    asyncio.run(puller.pull_all('foo'))

    directories_to_be_pulled = (
        [os.path.join('foo', dir) for dir in DIRECTORIES_FOLDER]
        + [os.path.join('foo', 'bar', dir) for dir in DIRECTORY_SUB_FOLDER]
    )
    mock_do_pull_in.assert_has_calls(
        [call(dir) for dir in directories_to_be_pulled], any_order=True)


@patch('pulla.pulla.Pulla.perform_git_pull')
def test_perform_git_pull_called_for_passed_directory(mock_perform_git_pull, puller):
    asyncio.run(puller.do_pull_in('foo'))

    mock_perform_git_pull.assert_called_once_with('foo')


@patch('pulla.pulla.Pulla.perform_git_pull')
@patch('pulla.pulla.Pulla.get_formatted_status_message')
def test_status_success_when_git_command_successful(
    mock_get_formatted_status_message, mock_perform_git_pull, puller
):
    mock_perform_git_pull.return_value = 0

    asyncio.run(puller.do_pull_in('foo'))

    mock_get_formatted_status_message.assert_called_once_with('foo', 0)


@patch('pulla.pulla.Pulla.perform_git_pull')
@patch('pulla.pulla.Pulla.get_formatted_status_message')
def test_status_fail_when_git_command_successful(
    mock_get_formatted_status_message, mock_perform_git_pull, puller
):
    mock_perform_git_pull.return_value = 128

    asyncio.run(puller.do_pull_in('foo'))

    mock_get_formatted_status_message.assert_called_once_with('foo', 128)


@patch('pulla.pulla.asyncio.create_subprocess_exec')
def test_pull_done_silently_when_no_verbosity(mock_create_subprocess, puller):
    mock_process = MagicMock()
    mock_process.wait = AsyncMock(return_value=128)
    mock_create_subprocess.return_value = mock_process

    status = asyncio.run(puller.perform_git_pull('foo'))

    mock_create_subprocess.assert_called_once_with(
        'git', 'pull', cwd='foo',
        stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
    assert status == 128


@patch('pulla.pulla.asyncio.create_subprocess_exec')
def test_pull_done_when_verbosity_level_set_one(mock_create_subprocess, puller):
    puller.verbosity = 1
    mock_process = MagicMock()
    mock_process.wait = AsyncMock(return_value=0)
    mock_create_subprocess.return_value = mock_process

    asyncio.run(puller.perform_git_pull('foo'))

    mock_create_subprocess.assert_called_once_with(
        'git', 'pull', '--verbose', cwd='foo', stdout=None, stderr=None)


def test_proper_fail_message_returned(puller):
    out = puller.get_formatted_status_message('foo', 128)
    assert out == 'foo                            [red]Fail[/red]'


def test_proper_success_message_returned(puller):
    out = puller.get_formatted_status_message('foo', 0)
    assert out == 'foo                            [green]Success[/green]'
