#!/usr/bin/env python

from __future__ import print_function

try:
    import unittest
    import unittest.mock
    from unittest.mock import patch
    from unittest.mock import call
except ImportError as e:
    import mock
    from mock import patch
    from mock import call

from pulla.pulla import Pulla

@patch('os.walk')
class test_pull_all(unittest.TestCase):

    @patch('pulla.pulla.is_this_a_git_dir')
    def test_pull_all_runs_pull_in_all_folders(self, is_git_mock, walk_mock):
        directories = ('a', 'b', 'c')
        walk_mock.return_value = [
            ('/foo', directories, ('baz',)),
            ('/foo/bar', ('d', 'e', 'f'), ('spam', 'eggs')),
            ]
        is_git_mock.return_value = True

        puller = Pulla()
        puller.pull_all('foo')

        calls_1 = [call('a'), call('b'), call('c')]
        is_git_mock.assert_has_calls(calls_1)

if __name__ == '__main__':
    unittest.main()
