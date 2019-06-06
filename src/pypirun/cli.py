# Copyright 2019, Oath Inc.
# Licensed under the terms of the BSD 3 Clause license. See LICENSE file in project root for terms.
"""
pypirun command line utility
"""
import os
import shutil
import subprocess  # nosec
import sys
import tempfile
from .arguments import parse_arguments, ParseError
from .utility import which


def interpreter_version(interpreter):
    """
    Get the version from the python interpreter
    """
    version = subprocess.check_output([interpreter, '--version'], stderr=subprocess.STDOUT).decode(errors='ignore').strip().split()[-1]  # nosec
    return version


def interpreter_parent(interpreter):
    """
    Get the parent python interpreter for interpreter (I.E the interpreter that created the virtualenv if it is an
    interpreter in a virtualenv.

    Returns
    =======
    str:
        parent interpreter
    """
    try:
        real_prefix = subprocess.check_output([interpreter, '-c', 'import sys;print(sys.real_prefix)']).decode(errors='ignore').strip()  # nosec
    except subprocess.CalledProcessError:  # pragma: no cover
        return interpreter
    try:
        major_minor = subprocess.check_output([interpreter, '-c', 'import sys;print(f"{sys.version_info.major}.{sys.version_info.minor}")']).decode(errors='ignore').strip()  # nosec
        basename = f'python{major_minor}'
    except subprocess.CalledProcessError:  # pragma: no cover
        basename = 'python3'

    bin_dir = os.path.join(real_prefix, 'bin')
    interpreter = os.path.join(bin_dir, basename)
    return interpreter


def install_and_run(package, command, interpreter, debug=False, no_cache_dir=False, upgrade_setuptools=False):
    """
    Install a package and run a command in a temporary Python virtualenv
    
    Parameters
    ==========
    package: str
        A string containing a comma seperated list of packages to install.
    
    command: str
        The command to run in the shell once the package is installed
        
    interpreter: str
        The python interpreter executable to use to create the virtualenv
    
    debug: bool, optional
        Print more useful debug output.  Default: False
    
    no_cache_dir: bool, optional
        If True, pass the no-cache-dir flag to the pip command to disable pip package caching.  Default: False
    
    upgrade_setuptools: bool, optional
        Upgrade setuptools after creating the virtualenv but before installing packages.  Default: False
    """
    packages = package.split(',')

    with tempfile.TemporaryDirectory() as tempdir:
        venv_dir = os.path.join(tempdir, '.venv')
        venv_bin = os.path.join(venv_dir, 'bin')
        venv_python = os.path.join(venv_bin, 'python')
        venv_pip = os.path.join(venv_bin, 'pip')

        pip_args = []
        if no_cache_dir:  # pragma: no cover
            pip_args = ['--no-cache-dir']

        # Create venv
        try:
            output = subprocess.check_output([interpreter, '-m', 'venv', venv_dir])  # nosec
        except subprocess.CalledProcessError:  # pragma: no cover
            print('Failed to create temporary virtualenv using the', interpreter, 'python interpreter')
            return 1
        if debug:
            if output.decode().strip():  # pragma: no cover
                print(output.decode().strip())

        if not os.path.exists(venv_pip):  # pragma: no cover
            output = subprocess.check_output([venv_python, '-m', 'pip', 'install', '--force-reinstall'] + pip_args + ['pip'], stderr=subprocess.STDOUT)  # nosec
            if debug:  # pragma: no cover
                print(output.decode())

        if upgrade_setuptools:  # pragma: no cover
            output = subprocess.check_output([venv_pip, 'install', '--upgrade'] + pip_args + ['setuptools'], stderr=subprocess.STDOUT)  # nosec
            if debug:  # pragma: no cover
                print(output.decode())

        venv_bin_before = set(os.listdir(venv_bin))

        # Install the package
        try:
            output = subprocess.check_output([venv_pip, 'install'] + pip_args + packages, stderr=subprocess.STDOUT)  # nosec
        except subprocess.CalledProcessError as error:   # pragma: no cover
            print(error.output.decode(), file=sys.stdout)
            return error.returncode

        venv_bin_after = set(os.listdir(venv_bin))

        if debug:  # pragma: no cover
            print(output.decode())
            print(f'Installed files: {list(venv_bin_after-venv_bin_before)}')

        # Run the command
        try:
            subprocess.check_call(f'{venv_dir}/bin/{command}', shell=True)  # nosec
        except subprocess.CalledProcessError as error:  # pragma: no cover
            return error.returncode
        return exit_ok()  # pragma: no cover


def exit_ok():
    """A python implementation of /bin/true that can be used for testing"""
    return 0


def main():
    """
    Command line interface entrypoint
    
    Returns
    =======
    int:
        return code from running the command
    """
    try:
        args = parse_arguments()
    except ParseError:
        return 1
    interpreter = args.interpreter
    command_file = args.command[0]
    command = ' '.join(args.command)
    if not interpreter:    # pragma: no cover
        interpreter = interpreter_parent(sys.executable)
    if not interpreter:    # pragma: no cover
        interpreter = which('python3')
    if not interpreter:    # pragma: no cover
        print('Unable to find python3 interpreter')
        return 1

    if args.always_install or not shutil.which(command_file):
        return install_and_run(package=args.package, command=command, interpreter=interpreter, debug=args.debug, no_cache_dir=args.no_cache_dir, upgrade_setuptools=args.upgrade_setuptools)

    try:
        subprocess.check_call(command, shell=True)  # nosec
    except subprocess.CalledProcessError as error:
        return error.returncode
    return 0  # pragma: no cover
