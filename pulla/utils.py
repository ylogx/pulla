import os

def is_this_a_git_dir(directory):
    possible_git_dir = os.path.join(directory, '.git')
    return os.path.isdir(possible_git_dir)

