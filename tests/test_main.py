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


class TestMain(unittest.TestCase):
    def setUp(self):
        self.argv_backup = sys.argv

    def tearDown(self):
        sys.argv = self.argv_backup

    @patch('pulla.main.Pulla.pull_all')
    def test_should_do_pull_in_subdirectories_if_no_args(self, mock_pull_all):
        sys.argv = ['dummy']
        main()
        curdir = os.path.abspath(os.curdir)
        mock_pull_all.assert_called_once_with(curdir)

    @patch('pulla.main.is_this_a_git_dir')
    @patch('pulla.main.Pulla.do_pull_in')
    def test_should_do_pull_in_current_directory_if_is_git_dir(self, mock_do_pull_in, mock_is_git_dir):
        curdir = os.path.abspath(os.curdir)
        sys.argv = ['dummy']
        mock_is_git_dir.return_value = True

        main()

        mock_do_pull_in.assert_called_once_with(curdir)

    @patch('pulla.main.Pulla')
    def test_should_set_verbosity_1_if_short_flag_passed(self, mock_pulla):
        sys.argv = ['dummy', '-v']
        main()
        mock_pulla.assert_called_once_with(verbosity=1, recursive=False)

    @patch('pulla.main.Pulla')
    def test_should_set_verbosity_1_if_long_flag_passed(self, mock_pulla):
        sys.argv = ['dummy', '--verbose']
        main()
        mock_pulla.assert_called_once_with(verbosity=1, recursive=False)


class AnyStringContaining(str):
    def __eq__(self, other):
        return self in other

if __name__ == '__main__':
    unittest.main()
