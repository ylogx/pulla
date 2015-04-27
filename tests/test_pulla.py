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
    @patch('multiprocessing.Process')
    def test_pull_all_runs_pull_in_all_folders(self, mock_multiprocess, mock_is_git, mock_walk):
        directories = ('a', 'b', 'c')
        mock_walk.return_value = [
            ('/foo', directories, ('baz',)),
            ('/foo/bar', ('d', 'e', 'f'), ('spam', 'eggs')),
            ]
        mock_is_git.return_value = True

        puller = Pulla()
        puller.pull_all('foo')

        calls = [call('a'), call('b'), call('c')]
        mock_is_git.assert_has_calls(calls)

        calls_for_process_creation = [
            call(args=['a'], target=puller.do_pull_in),
            call().start(),
            call(args=['b'], target=puller.do_pull_in),
            call().start(),
            call(args=['c'], target=puller.do_pull_in),
            call().start(),
        ]
        mock_multiprocess.assert_has_calls(calls_for_process_creation)

if __name__ == '__main__':
    unittest.main()
