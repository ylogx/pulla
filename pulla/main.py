#!/usr/bin/env python3
import sys
import os

class Pulla:
    ''' Pulla main class
    '''
    def __init__(self, verbosity=None, recursive=None):
        self.verbosity = verbosity
        self.recursive = recursive

    def pull_all(self, folder):
        for (dirpath, dirnames, filenames) in os.walk(folder):
            for dirname in dirnames:
                possible_git_dir = os.path.join(dirname, '.git')
                if os.path.isdir(possible_git_dir):
                    print('Going into', os.path.join(dirname))
                    os.chdir(dirname)
                    cmd = 'git pull'
                    if self.verbosity:
                        cmd += ' --verbose'
                    print('Running:', cmd)
                    if self.verbosity:
                        print('----------------------')
                    #response = input('Do you want to proceed: ')
                    #if response in ['y', 'yes', 'yup', 'yo', 'doit']:
                    os.system(cmd)
                    if self.verbosity:
                        print('----------------------')
                    os.chdir(os.path.join(dirpath, dirname, '..'))
            if not self.recursive:
                break
        return None

def main():
    ''' Main
    '''
    curdir = os.path.abspath(os.curdir)
    print('Current Directory is: ', curdir)
    pulla = Pulla(verbosity=True, recursive=False)
    pulla.pull_all(curdir)

if __name__ == '__main__':
    sys.exit(main())
