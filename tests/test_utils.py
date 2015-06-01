#!/usr/bin/env python

from __future__ import print_function

try:
    import unittest
    import unittest.mock
    from unittest.mock import call, patch
except ImportError as e:
    import unittest2 as unittest
    import mock
    from mock import call, patch

import os

from pulla.utils import is_this_a_git_dir, get_git_version


class TestThatNeedAGitDirectory(unittest.TestCase):
    def test_is_this_a_git_dir_returns_false_for_non_git_dir(self):
        random_directory = 'random_non_git_directory'
        self.assertFalse(is_this_a_git_dir(random_directory))

    @patch('os.path.isdir')
    def test_is_this_a_git_dir_returns_true_for_git_dir(self, mock_is_dir):
        test_dir = 'dummy_dir'
        possible_git_dir = os.path.join(test_dir, '.git')
        mock_is_dir.return_value = True

        output = is_this_a_git_dir(test_dir)

        mock_is_dir.assert_called_once_with(possible_git_dir)
        self.assertTrue(output)

    def test_is_this_a_git_dir_returns_false_for_null_dir(self):
        self.assertFalse(is_this_a_git_dir(None))


class TestGetGitVersion(unittest.TestCase):
    def setUp(self):
        self.GIT_VERSION_RESPONSE = 'git version 2.2.2'

    @unittest.skip
    @patch.object('os.popen', 'read')
    def test_correct_git_version_returned(self, mock_popen):
        mock_popen.return_value = self.GIT_VERSION_RESPONSE

        git_version = get_git_version()

        self.assertEqual(git_version, '2.2.2')

    @patch('os.popen')
    def test_opened_stream_is_closed(self, mock_popen):
        get_git_version()

        calls = [call('git --version'), call().read(), call().close(), ]
        mock_popen.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
