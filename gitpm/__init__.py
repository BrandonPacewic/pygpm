# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
gitpm - A git repository manager
"""

from gitpm.core import __version__
from gitpm.logging import init_logging

__all__ = ["__version__"]

init_logging()
