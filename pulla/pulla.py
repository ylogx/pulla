from __future__ import print_function

import os
from pulla.utils import is_this_a_git_dir

VERSION_WITH_C_FLAG_SUPPORT = "1.8.5"

class Pulla:
    ''' Pulla class
    '''
    def __init__(self, verbosity=None, recursive=None):
        self.verbosity = verbosity
        self.recursive = recursive

    def pull_all(self, folder):
        for (dirpath, dirnames, _) in os.walk(folder):
            for directory in dirnames:
                if is_this_a_git_dir(directory):
                    self.do_pull_in(directory)
            if not self.recursive:
                break
        return None

    def do_pull_in(self, directory):
        if self.verbosity:
            print('----------------------')
        status = self.perform_git_pull(directory)
        status_msg = 'Fail'
        if status == 0:
            status_msg = 'Success'
        print('{0:<20} {1:<10}'.format(os.path.join(directory), status_msg))
        if self.verbosity:
            print('----------------------')


    def perform_git_pull(self, directory):
        can_use_c_flag = self.get_git_version() >= VERSION_WITH_C_FLAG_SUPPORT
        if can_use_c_flag:
            cmd = 'git -C ' + directory + ' pull'
        else:
            os.chdir(directory)
            cmd = 'git pull'
        if self.verbosity:
            cmd += ' --verbose'
        else:
            cmd += ' &> /dev/null'
        status = os.system(cmd)
        if not can_use_c_flag:
            os.chdir('..')
        return status

    def get_git_version(self):
        version_string = os.popen('git --version').read()
        return version_string.split()[-1]
