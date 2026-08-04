import asyncio
import os

from .utils import is_this_a_git_dir
from .logger import Logger
from .logger import verbosity_level


class Pulla:
    """ Pulla class
    """

    def __init__(self, verbosity=0, recursive=None):
        self.verbosity = verbosity
        self.recursive = recursive
        self.max_dir_length = 20
        self.logger = Logger(self.verbosity)

    async def pull_all(self, folder):
        git_dirs = []
        for (dirpath, dirnames, _) in os.walk(os.path.abspath(folder)):
            self.max_dir_length = self.find_max_dir_length(dirnames)
            for directory in dirnames:
                directory = os.path.join(dirpath, directory)
                if is_this_a_git_dir(directory):
                    git_dirs.append(directory)
            if not self.recursive:
                break
        await asyncio.gather(*(self.do_pull_in(d) for d in git_dirs))

    def find_max_dir_length(self, directories):
        max_dir_length = 20
        for directory in directories:
            if len(directory) > self.max_dir_length:
                max_dir_length = len(directory)
        return max_dir_length

    async def do_pull_in(self, directory):
        self.logger.print_log('----------------------',
                              verbosity_level['high'])
        status = await self.perform_git_pull(directory)

        self.logger.print_log(self.get_formatted_status_message(
            directory, status), verbosity_level['low'])
        self.logger.print_log('----------------------',
                              verbosity_level['high'])

    async def perform_git_pull(self, directory):
        args = ['git', 'pull']
        stdout = stderr = None
        if self.verbosity != 0:
            args.append('--verbose')
        else:
            stdout = stderr = asyncio.subprocess.DEVNULL

        process = await asyncio.create_subprocess_exec(
            *args, cwd=directory, stdout=stdout, stderr=stderr)
        return await process.wait()

    def get_formatted_status_message(self, directory, status):
        directory = os.path.basename(directory)
        status_msg = '[red]Fail[/red]'
        if status == GitStatus.SUCCESS:
            status_msg = '[green]Success[/green]'
        format_string = '{0:<' + str(self.max_dir_length + 10) + '} {1:<10}'
        return format_string.format(os.path.join(directory), status_msg)

class GitStatus:
    SUCCESS = 0
