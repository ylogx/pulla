#!/usr/bin/env python3
import sys
import os
import argparse

class Pulla:
    ''' Pulla main class
    '''
    def __init__(self, verbosity=None, recursive=None):
        self.verbosity = verbosity
        self.recursive = recursive

    def pull_all(self, folder):
        for (dirpath, dirnames, _) in os.walk(folder):
            for dirname in dirnames:
                if is_this_a_git_dir(dirname):
                    self.do_pull_in(dirname)
                    os.chdir(os.path.join(dirpath, dirname, '..'))
                    #TODO: chdir needs to happen in do_pull_in function
            if not self.recursive:
                break
        return None

    def do_pull_in(self, directory):
        os.chdir(directory)
        cmd = 'git pull'
        if self.verbosity:
            cmd += ' --verbose'
        print(os.path.join(directory), ':', cmd)
        if self.verbosity:
            print('----------------------')
        #response = input('Do you want to proceed: ')
        #if response in ['y', 'yes', 'yup', 'yo', 'doit']:
        os.system(cmd)
        if self.verbosity:
            print('----------------------')

def is_this_a_git_dir(directory):
     possible_git_dir = os.path.join(directory, '.git')
     return os.path.isdir(possible_git_dir)

def main():
    ''' Main
    '''
    # Parse command line arguments
    #usage = "%prog [-f credential_file]"
    #parser = ArgumentParser(usage=usage)
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", type=str, dest="folder",
                        help="Update the repos in this folder")
    parser.add_argument("-v", "--verbose", required=False, dest="verbosity",
                        type=int, default=1, help="Verbosity")
    #parser.add_argument('otherthings', nargs='*')
    #args = parser.parse_args()
    args, otherthings = parser.parse_known_args()
    argc = len(otherthings)


    directory = os.path.abspath(os.curdir)
    if args.folder:
        directory = args.folder

    print('Directory is: ', directory)
    pulla = Pulla(verbosity=True, recursive=False)

    if is_this_a_git_dir(directory):
        pulla.do_pull_in(directory)
    else:
        pulla.pull_all(directory)

if __name__ == '__main__':
    sys.exit(main())
