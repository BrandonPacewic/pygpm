"""gitpm - A git repository manager
"""

# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

from gitpm.core import __version__
from gitpm.logging import init_logging

__all__ = ["__version__"]

# Must be called before any call to gitpm.logging.get_logger() which
# happens at import time of most modules.
init_logging()
