#!/usr/bin/env python
#=====================
from __future__ import print_function

try:
    import unittest
    import unittest.mock
    from unittest.mock import patch
except ImportError as e:
    import unittest2 as unittest
    import mock
    from mock import patch

import os
import shutil

from pulla.utils import is_this_a_git_dir

class test_that_need_a_git_directory(unittest.TestCase):
    def test_is_this_a_git_dir_returns_false_for_non_git_dir(self):
        random_directory = 'random_non_git_directory'
        self.assertFalse(is_this_a_git_dir(random_directory))

    @patch('os.path.isdir')
    def test_is_this_a_git_dir_returns_true_for_git_dir(self, mock_is_dir):
        test_dir= 'dummy_dir'
        possible_git_dir = test_dir + '/.git'
        mock_is_dir.return_value = True

        output = is_this_a_git_dir(test_dir)

        mock_is_dir.assert_called_once_with(possible_git_dir)
        self.assertTrue(output)

    def test_is_this_a_git_dir_returns_false_for_null_dir(self):
        self.assertFalse(is_this_a_git_dir(None))

if __name__ == '__main__':
    unittest.main()
