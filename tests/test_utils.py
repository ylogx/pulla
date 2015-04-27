#!/usr/bin/env python
#=====================
from __future__ import print_function

try:
    import unittest
    import unittest.mock
    from unittest.mock import patch
except ImportError as e:
    import mock
    from mock import patch

import os
import shutil

from pulla.main import is_this_a_git_dir

class test_that_need_a_git_directory(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'dummy_dir'
        self.test_dir_git = self.test_dir + '/.git/'
        try:
            os.makedirs(self.test_dir_git)
        except OSError as e:
            print(e)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_is_this_a_git_dir_returns_false_for_non_git_dir(self):
        random_directory = 'random_non_git_directory'
        self.assertFalse(is_this_a_git_dir(random_directory))

    def test_is_this_a_git_dir_returns_true_for_git_dir(self):
        self.assertTrue(is_this_a_git_dir(self.test_dir))

if __name__ == '__main__':
    unittest.main()
