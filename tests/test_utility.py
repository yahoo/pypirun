import os
import shutil
import unittest

from pypirun import utility


class TestUtility(unittest.TestCase):
    test_key = 'OUROATH_UTILITY'

    def tearDown(self):
        try:
            del os.environ[self.test_key]
        except KeyError:
            pass

    def test__env_bool__default(self):
        self.assertTrue(utility.env_bool(self.test_key, True))
        self.assertFalse(utility.env_bool(self.test_key, False))

    def test__env_bool__true(self):
        os.environ[self.test_key] = 'True'
        self.assertTrue(utility.env_bool(self.test_key, False))

    def test__env_bool__false(self):
        os.environ[self.test_key] = 'False'
        self.assertFalse(utility.env_bool(self.test_key, True))

    def test__which__allow_symlink(self):
        result = utility.which('python3', allow_symlink=True)
        self.assertEqual(result, shutil.which('python3'))

    def test__which__allow_symlink__false(self):
        result = utility.which('python3', allow_symlink=False)
