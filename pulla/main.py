#!/usr/bin/env python3

import asyncio
import os
from typing import Optional

import typer

from . import __version__
from .pulla import Pulla
from .utils import is_this_a_git_dir
from .logger import verbosity_level

app = typer.Typer(add_completion=False)


def print_version():
    print('Pulla version %s' % __version__)
    print('Copyright (c) 2015 by Shubham Chaudhary.')
    print('License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>')
    print('This is free software: you are free to change and redistribute it.')
    print('There is NO WARRANTY, to the extent permitted by law.')


def version_callback(value: bool):
    if value:
        print_version()
        raise typer.Exit()


@app.command()
def main(
    folder: Optional[str] = typer.Option(
        None, '-f', '--folder',
        help='Update the repos in this folder'),
    verbose: bool = typer.Option(
        False, '-v', '--verbose',
        help='Show verbose information. Higher verbosity can be selected'
        ' by --verbosity flag'),
    verbosity: Optional[int] = typer.Option(
        None, '-l', '--verbosity',
        min=1, max=3,
        help='Set higher verbosity level for more detailed information:'
        ' 1. Low, 2. Medium, 3. High'),
    version: Optional[bool] = typer.Option(
        None, '-V', '--version',
        callback=version_callback, is_eager=True,
        help='Print the version number and exit'),
):
    if verbose and verbosity is not None:
        raise typer.BadParameter(
            '-v/--verbose and -l/--verbosity are mutually exclusive')

    directory = os.path.abspath(os.curdir)
    if folder:
        directory = folder

    resolved_verbosity = 0
    if verbose:
        resolved_verbosity = verbosity_level['low']
    elif verbosity:
        resolved_verbosity = verbosity

    puller = Pulla(verbosity=resolved_verbosity, recursive=False)

    asyncio.run(_pull(puller, directory))


async def _pull(puller, directory):
    if is_this_a_git_dir(directory):
        await puller.do_pull_in(directory)
    else:
        await puller.pull_all(directory)


if __name__ == '__main__':
    app()
