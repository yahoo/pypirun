# Copyright 2019, Oath Inc.
# Licensed under the terms of the BSD 3 Clause license. See LICENSE file in project root for terms.
"""
pypirun command line utility
"""
import json
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


def install_and_run(package, command, interpreter, debug=False, no_cache_dir=False, upgrade_setuptools=False):
    packages = package.split(',')

    with tempfile.TemporaryDirectory() as tempdir:
        venv_dir = os.path.join(tempdir, '.venv')
        venv_bin = os.path.join(venv_dir, 'bin')
        venv_python = os.path.join(venv_bin, 'python3')
        venv_pip = os.path.join(venv_bin, 'pip')

        pip_args = []
        if no_cache_dir:  # pragma: no cover
            pip_args = ['--no-cache-dir']

        # Create venv
        output = subprocess.check_output([interpreter, '-m', 'venv', venv_dir])  # nosec
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
        return 0


def main():
    try:
        args = parse_arguments()
    except ParseError:
        return 1
    interpreter = args.interpreter
    command_file = args.command[0]
    command = ' '.join(args.command)
    if not interpreter:    # pragma: no cover
        interpreter = which('python3')

    if args.always_install or not shutil.which(command_file):
        return install_and_run(package=args.package, command=command, interpreter=interpreter, debug=args.debug, no_cache_dir=args.no_cache_dir, upgrade_setuptools=args.upgrade_setuptools)

    try:
        subprocess.check_call(command, shell=True)  # nosec
    except subprocess.CalledProcessError as error:
        return error.returncode
    return 0
