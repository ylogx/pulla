from __future__ import print_function

import os
from pulla.utils import is_this_a_git_dir

class Pulla:
    ''' Pulla class
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
        print(os.path.join(directory), ':')
        if self.verbosity:
            print('----------------------')
        #response = input('Do you want to proceed: ')
        #if response in ['y', 'yes', 'yup', 'yo', 'doit']:
        os.system(cmd)
        if self.verbosity:
            print('----------------------')

