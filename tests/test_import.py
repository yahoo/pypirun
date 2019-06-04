#!/usr/bin/env python
"""
test_pypirun
"""
import unittest


class TestImport(unittest.TestCase):

    def test__module__import(self):
        import pypirun


if __name__ == '__main__':
    unittest.main()
