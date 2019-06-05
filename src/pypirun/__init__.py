# Copyright 2019, Oath Inc.
# Licensed under the terms of the BSD 3 Clause license. See LICENSE file in project root for terms.
"""
pypirun module
"""
from typing import List
import pkg_resources


__all__: List[str] = []
__copyright__: str = "Copyright 2019, Oath Inc."
__version__: str = pkg_resources.get_distribution("pypirun").version
