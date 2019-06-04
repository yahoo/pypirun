# Copyright 2019, Oath Inc.
# Licensed under the terms of the BSD 3 Clause license. See LICENSE file in project root for terms.
"""
pypirun utility functions
"""
import os
import shutil


def env_bool(variable_name, default=True):
    """
    Interperate an environment variable as a boolean value.

    Parameters
    ==========
    variable_name: str
        Environment key to get the value for

    default: bool
        Value to return if the environment variable does not exists

    Returns
    =======
    bool: Value from the environment variable
    """
    true_strings = ['true', 'on', '1']

    value = os.environ.get(variable_name, str(default)).lower()

    if value in true_strings:
        return True
    return False


def which(filename, allow_symlink=False):
    """
    Search the path for an executable, optionally ignoring symlinks

    Parameters
    ==========
    filename: str
        Filename to search for

    allow_symlink: bool
        If True, return filenames that are symlinks
    """
    if allow_symlink:
        return shutil.which(filename)

    search_dirs = os.environ.get('PATH', '').split(':')
    for directory in search_dirs:  # pragma: no cover
        full_filename = os.path.join(directory, filename)
        if not os.path.exists(full_filename):
            continue
        if os.path.islink(full_filename):
            link = os.readlink(full_filename)
            if '/' in link:
                return os.path.abspath((os.path.join(directory, link)))
            continue
        return full_filename
