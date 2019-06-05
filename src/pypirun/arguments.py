# Copyright 2019, Oath Inc.
# Licensed under the terms of the BSD 3 Clause license. See LICENSE file in project root for terms.
"""
pypirun module command line parsing functions
"""
import argparse
import os
import sys
from .utility import env_bool


class ParseError(Exception):
    """
    CLI Argument parsing error
    """
    pass


def parse_arguments() -> argparse.Namespace:
    """
    Parse the command line arguments

    Returns
    =======
    argparse.Namespace:
        Arguments parsed from the command line

    Raises
    ======
    ParseError - Unable to parse the command line arguments
    """

    default_interpreter = os.environ.get('BASE_PYTHON', None)
    debug = env_bool('PYPIRUN_DEBUG', False)

    parser = argparse.ArgumentParser()
    parser.add_argument('--interpreter', default=default_interpreter, help='Python interpreter to use')
    parser.add_argument('--debug', default=debug, action='store_true', help='Enable debug output')
    parser.add_argument('--always_install', default=False, action='store_true', help='Install the command even if it exists in the path')
    parser.add_argument('--no-cache-dir', default=False, action='store_true', help="Disable the pip cache when installing")
    parser.add_argument('--upgrade_setuptools', default=False, action='store_true', help="Upgrade setuptools before installing")
    parser.add_argument('package', type=str, help='Package the command is in')
    parser.add_argument('command', nargs='*', help='Command to run')

    if len(sys.argv) < 2:
        parser.print_usage()
        raise ParseError('Unable to parse arguments')

    argv = []
    command = []
    in_command = False
    for argument in sys.argv[1:]:
        if not in_command and argument.startswith('--'):
            argv.append(argument)
            continue
        in_command = True
        command.append(argument)

    argv += ['package', 'command']

    if len(command) < 2:
        parser.print_usage()
        raise ParseError('Insufficient arguments provided')

    args = parser.parse_args(args=argv)
    args.package = command[0]
    args.command = command[1:]

    return args
