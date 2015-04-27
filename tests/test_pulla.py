#!/usr/bin/env python

from __future__ import print_function
from itertools import chain

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
@patch('pulla.pulla.is_this_a_git_dir')
@patch('multiprocessing.Process')
class test_pull_all(unittest.TestCase):

    def test_pull_all_starts_process_for_folders_in_passed_directory_when_not_recursive(self, mock_multiprocess, mock_is_git, mock_walk):
        directories_folder = ('a', 'b', 'c')

        mock_walk.return_value = [
            ('/foo', directories_folder, ('baz',)),
            ('/foo/bar', ('d', 'e', 'f'), ('spam', 'eggs')),
            ]
        mock_is_git.return_value = True

        puller = Pulla()
        puller.pull_all('foo')

        calls = [call('a'), call('b'), call('c')]
        mock_is_git.assert_has_calls(calls)

        calls_for_process_creation = self.get_calls_for_process_creation(
            directories_folder,
            puller
        )
        mock_multiprocess.assert_has_calls(calls_for_process_creation)

    def test_pull_all_starts_process_for_all_folders_when_recursive(self, mock_multiprocess, mock_is_git, mock_walk):
        directories_folder = ('a', 'b', 'c')
        directory_sub_folder = ('d', 'e', 'f')
        mock_walk.return_value = [
            ('/foo', directories_folder, ('baz',)),
            ('/foo/bar', directory_sub_folder, ('spam', 'eggs')),
            ]
        mock_is_git.return_value = True

        puller = Pulla(recursive=True)
        puller.pull_all('foo')

        directories_to_be_pulled = directories_folder + directory_sub_folder

        calls_for_process_creation = self.get_calls_for_process_creation(
            directories_to_be_pulled,
            puller
        )
        mock_multiprocess.assert_has_calls(calls_for_process_creation)

    def get_calls_for_process_creation(self, directories_to_be_pulled, puller):
        '''
        :return: list with format
        [
            call(args=['dir1'], target=puller.do_pull_in),
            call().start(),
            call(args=['dir2'], target=puller.do_pull_in),
            call().start(),
        ]
        '''
        calls_for_process_creation = list(chain.from_iterable(
            (
                call(args=[dir], target=puller.do_pull_in),
                call().start()
            ) for dir in directories_to_be_pulled
        ))
        return calls_for_process_creation

if __name__ == '__main__':
    unittest.main()
