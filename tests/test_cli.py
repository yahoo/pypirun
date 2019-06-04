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

    def test__no_args(self):
        sys.argv = ['pypirun']
        self.assertEqual(cli.main(), 1)

    def test__run__already_installed(self):
        sys.argv = ['pypirun', '--debug', '.', 'pypirun']
        self.assertEqual(cli.main(), 1)

    def test__run__no_cache_dir(self):
        sys.argv = ['pypirun', '--no-cache-dir', '.', 'pypirun']
        self.assertEqual(cli.main(), 1)

    def test__run__upgrade_setuptools(self):
        sys.argv = ['pypirun', '--upgrade_setuptools', '.', 'pypirun']
        cli.main()

    def test__run__forced_install(self):
        sys.argv = ['pypirun', '--debug', '--always_install', '.', 'pypirun']
        cli.main()

    def test__run__invalid_command(self):
        sys.argv = ['pypirun', '--debug', '--always_install', '.', 'pypirun', 'fabzkkkks']
        cli.main()

    def test__interpreter_version__(self):
        result = cli.interpreter_version(sys.executable)
        self.assertTrue(result.startswith('3'))
