import os


def is_this_a_git_dir(directory):
    if directory is None:
        return False

    possible_git_dir = os.path.join(directory, '.git')
    return os.path.isdir(possible_git_dir)


def get_git_version():
    han = os.popen('git --version')
    version_string = han.read()
    han.close()
    return version_string.split()[-1]
