from __future__ import print_function

import os
import multiprocessing
from colorama import Fore

from .utils import is_this_a_git_dir, get_git_version
from .logger import Logger
from .logger import verbosity_level

VERSION_WITH_C_FLAG_SUPPORT = "1.8.5"


class Pulla:
    """ Pulla class
    """

    def __init__(self, verbosity=0, recursive=None):
        self.verbosity = verbosity
        self.recursive = recursive
        self.max_dir_length = 20
        self.logger = Logger(self.verbosity)

    def pull_all(self, folder):
        for (_, directories, _) in os.walk(folder):
            threads = []
            self.max_dir_length = self.find_max_dir_length(directories)
            for directory in directories:
                if is_this_a_git_dir(directory):
                    process = multiprocessing.Process(target=self.do_pull_in,
                                                      args=[directory])
                    process.start()
                    threads.append(process)
            if not self.recursive:
                break
        return None

    def find_max_dir_length(self, directories):
        max_dir_length = 20
        for directory in directories:
            if len(directory) > self.max_dir_length:
                max_dir_length = len(directory)
        return max_dir_length

    def do_pull_in(self, directory):
        self.logger.print_log('----------------------',
                              verbosity_level['high'])
        status = self.perform_git_pull(directory)

        self.logger.print_log(self.get_formatted_status_message(
            directory, status), verbosity_level['low'])
        self.logger.print_log('----------------------',
                              verbosity_level['high'])

    def perform_git_pull(self, directory):
        can_use_c_flag = get_git_version() >= VERSION_WITH_C_FLAG_SUPPORT
        if can_use_c_flag:
            cmd = 'git -C ' + directory + ' pull'
        else:
            os.chdir(directory)
            cmd = 'git pull'
        if self.verbosity is not 0:
            cmd += ' --verbose'
        else:
            cmd += ' &> /dev/null'
        status = os.system(cmd)
        if not can_use_c_flag:
            os.chdir('..')
        return status

    def get_formatted_status_message(self, directory, status):
        status_msg = Fore.RED + 'Fail' + Fore.RESET
        if status == GitStatus.SUCCESS:
            status_msg = Fore.GREEN + 'Success' + Fore.RESET
        format_string = '{0:<' + str(self.max_dir_length + 10) + '} {1:<10}'
        return format_string.format(os.path.join(directory), status_msg)

class GitStatus:
    SUCCESS = 0
