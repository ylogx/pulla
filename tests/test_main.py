#!/usr/bin/env python

from __future__ import print_function

import os
import sys

try:
    import unittest
    import unittest.mock
    from unittest.mock import patch
    from unittest.mock import call
except ImportError as e:
    import mock
    from mock import patch
    from mock import call

from pulla.main import main


@patch('pulla.main.Pulla.pull_all')
@patch('pulla.main.Pulla.do_pull_in')
class TestMain(unittest.TestCase):
    def setUp(self):
        self.argv_backup = sys.argv

    def tearDown(self):
        sys.argv = self.argv_backup

    @patch('pulla.main.is_this_a_git_dir')
    def test_should_do_pull_in_subdirectories_if_no_args(self, mock_is_git_dir,
                                                         mock_do_pull_in,
                                                         mock_pull_all):
        self.ensure_no_git_pull_done(mock_do_pull_in, mock_pull_all)
        sys.argv = ['dummy']
        mock_is_git_dir.return_value = False

        main()

        curdir = os.path.abspath(os.curdir)
        mock_pull_all.assert_called_once_with(curdir)

    @patch('pulla.main.is_this_a_git_dir')
    def test_should_do_pull_in_current_directory_if_is_git_dir(
        self, mock_is_git_dir, mock_do_pull_in, mock_pull_all
    ):
        self.ensure_no_git_pull_done(mock_do_pull_in, mock_pull_all)
        curdir = os.path.abspath(os.curdir)
        sys.argv = ['dummy']
        mock_is_git_dir.return_value = True

        main()

        mock_do_pull_in.assert_called_once_with(curdir)

    @patch('pulla.main.Pulla')
    def test_should_set_verbosity_1_if_short_flag_passed(self, mock_pulla,
                                                         mock_do_pull_in,
                                                         mock_pull_all):
        self.ensure_no_git_pull_done(mock_do_pull_in, mock_pull_all)
        sys.argv = ['dummy', '-v']
        main()
        mock_pulla.assert_called_once_with(verbosity=1, recursive=False)

    @patch('pulla.main.Pulla')
    def test_should_set_verbosity_1_if_long_flag_passed(self, mock_pulla,
                                                        mock_do_pull_in,
                                                        mock_pull_all):
        self.ensure_no_git_pull_done(mock_do_pull_in, mock_pull_all)
        sys.argv = ['dummy', '--verbose']
        main()
        mock_pulla.assert_called_once_with(verbosity=1, recursive=False)

    def ensure_no_git_pull_done(self, mock_do_pull_in, mock_pull_all):
        mock_do_pull_in.return_value = 0
        mock_pull_all.return_value = 0


@patch('pulla.main.print_version')
class TestVersion(unittest.TestCase):
    def test_should_print_version_and_exit_with_short_flag(self, mock_print_version):
        sys.argv = ['dummy', '-V']
        out = main()
        mock_print_version.assert_called_once_with()
        self.assertEqual(out, 0)

    def test_should_print_version_and_exit_with_long_flag(self, mock_print_version):
        sys.argv = ['dummy', '--version']
        out = main()
        mock_print_version.assert_called_once_with()
        self.assertEqual(out, 0)

class AnyStringContaining(str):
    def __eq__(self, other):
        return self in other


if __name__ == '__main__':
    unittest.main()
