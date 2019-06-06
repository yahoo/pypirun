import os
import sys
import unittest
from pypirun import cli


class TestClass(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._argv = sys.argv

    def tearDown(self):
        super().tearDown()
        sys.argv = self._argv

    @unittest.skipIf(not os.path.exists('setup.py'), "Not in package directory, no package to test against")
    def test__install_and_run(self):
        rc = cli.install_and_run(package='.', command='pypirun_true', interpreter=cli.interpreter_parent(sys.executable))
        self.assertEqual(rc, 0)

    def test__no_args(self):
        sys.argv = ['pypirun']
        self.assertEqual(cli.main(), 1)

    @unittest.skipIf(not os.path.exists('setup.py'), "Not in package directory, no package to test against")
    def test__run__already_installed(self):
        sys.argv = ['pypirun', '--debug', '.', 'pypirun']
        self.assertEqual(cli.main(), 1)

    @unittest.skipIf(not os.path.exists('setup.py'), "Not in package directory, no package to test against")
    def test__run__no_cache_dir(self):
        sys.argv = ['pypirun', '--no-cache-dir', '.', 'pypirun']
        self.assertEqual(cli.main(), 1)

    @unittest.skipIf(not os.path.exists('setup.py'), "Not in package directory, no package to test against")
    def test__run__upgrade_setuptools(self):
        sys.argv = ['pypirun', '--upgrade_setuptools', '.', 'pypirun']
        self.assertEqual(cli.main(), 1)

    @unittest.skipIf(not os.path.exists('setup.py'), "Not in package directory, no package to test against")
    def test__run__forced_install(self):
        sys.argv = ['pypirun', '--debug', '--always_install', '.', 'pypirun']
        self.assertEqual(cli.main(), 1)

    @unittest.skipIf(not os.path.exists('setup.py'), "Not in package directory, no package to test against")
    def test__run__invalid_command(self):
        sys.argv = ['pypirun', '--debug', '--always_install', '.', 'pypirun', 'fabzkkkks']
        self.assertEqual(cli.main(), 1)

    @unittest.skipIf(not os.path.exists('setup.py'), "Not in package directory, no package to test against")
    def test__run__good_return(self):
        sys.argv = ['pypirun', '--debug', '--always_install', '.', 'pypirun_true']
        self.assertEqual(cli.main(), 0)

    def test__interpreter_version__(self):
        result = cli.interpreter_version(sys.executable)
        self.assertTrue(result.startswith('3'))
