#!/usr/bin/env python3

from __future__ import print_function

import sys
import os
import argparse

from . import __version__
from .pulla import Pulla
from .utils import is_this_a_git_dir
from .logger import verbosity_level


def print_version():
    print('Pulla version %s' % __version__)
    print('Copyright (c) 2015 by Shubham Chaudhary.')
    print('License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>')
    print('This is free software: you are free to change and redistribute it.')
    print('There is NO WARRANTY, to the extent permitted by law.')


def parse_known_args():
    """ Parse command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder',
                        type=str,
                        dest='folder',
                        help='Update the repos in this folder')
    parser.add_argument('-V', '--version',
                        action='store_true',
                        dest='version',
                        help='Print the version number and exit')
    mutually_exclusive_group = parser.add_mutually_exclusive_group()

    mutually_exclusive_group.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show verbose information.'
        ' Higher verbosity can be selected by --verbosity'
        ' flag')
    mutually_exclusive_group.add_argument(
        '-l', '--verbosity',
        type=int,
        help='Set higher verbosity level for more detailed'
        ' information: 1. Low, 2. Medium, 3. High',
        choices=range(1, 4))

    args, otherthings = parser.parse_known_args()
    return args, otherthings


def main():
    """ Main
    """
    args, otherthings = parse_known_args()

    if args.version:
        print_version()
        return 0

    directory = os.path.abspath(os.curdir)
    if args.folder:
        directory = args.folder

    verbosity = 0
    if args.verbose:
        verbosity = verbosity_level['low']
    elif args.verbosity:
        verbosity = args.verbosity

    pulla = Pulla(verbosity=verbosity, recursive=False)

    if is_this_a_git_dir(directory):
        pulla.do_pull_in(directory)
    else:
        pulla.pull_all(directory)


if __name__ == '__main__':
    sys.exit(main())
