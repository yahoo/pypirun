import argparse
import os
import sys
import unittest
import pypirun.arguments


class TestArguments(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orig_cwd = os.getcwd()
        self.orig_argv = sys.argv

    def tearDown(self):
        super().tearDown()
        os.chdir(self.orig_cwd)
        sys.argv = self.orig_argv

    def test_parse_arguments_defaults(self):
        sys.argv = ['parse_arguments']
        with self.assertRaises(pypirun.arguments.ParseError):
            result = pypirun.arguments.parse_arguments()

    def test_parse_arguments__missing_command(self):
        sys.argv = ['parse_arguments', 'foo']
        default_interpreter = os.environ.get('BASE_PYTHON', None)
        with self.assertRaises(pypirun.arguments.ParseError):
            result = pypirun.arguments.parse_arguments()

    def test_parse_arguments_defaults__package_command(self):
        sys.argv = ['parse_arguments', 'foo', 'bar']
        default_interpreter = os.environ.get('BASE_PYTHON', None)
        result = pypirun.arguments.parse_arguments()
        self.assertIsInstance(result, argparse.Namespace)
        self.assertEqual(result.interpreter, default_interpreter)
        self.assertFalse(result.debug)
        self.assertFalse(result.always_install)
        self.assertFalse(result.upgrade_pip)
        self.assertFalse(result.upgrade_setuptools)
        self.assertEqual(result.package, 'foo')
        self.assertEqual(result.command, ['bar'])

    def test_parse_arguments_module(self):
        sys.argv = ['parse_arguments', '-m', 'foo', 'bar']
        default_interpreter = os.environ.get('BASE_PYTHON', None)
        result = pypirun.arguments.parse_arguments()
        self.assertIsInstance(result, argparse.Namespace)
        self.assertEqual(result.interpreter, default_interpreter)
        self.assertFalse(result.debug)
        self.assertFalse(result.always_install)
        self.assertFalse(result.upgrade_pip)
        self.assertFalse(result.upgrade_setuptools)
        self.assertEqual(result.module, 'bar')
        self.assertEqual(result.package, 'foo')
        self.assertEqual(result.command, [])
