# Copyright 2019, Oath Inc.
# Licensed under the terms of the BSD 3 Clause license. See LICENSE file in project root for terms.
"""
pypirun module
"""
from typing import List
from importlib.metadata import version, PackageNotFoundError



__all__: List[str] = []
__copyright__: str = "Copyright 2019, Oath Inc."
try:
    __version__ = version("pypirun")
except PackageNotFoundError:
    __version__ = '0.0.0'
