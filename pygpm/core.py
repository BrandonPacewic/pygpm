# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
Core constants used throughout pygpm.
"""

import os
import platform

__version__ = "0.1.0"

HOME = os.getenv("HOME", os.getenv("USERPROFILE"))
XDG_CACHE_DIR = os.getenv(
    "XDG_CACHE_HOME",
    os.path.join(
        HOME if HOME is not None else "",
        ".cache"))
XDG_CONFIG_DIR = os.getenv(
    "XDG_CONFIG_HOME",
    os.path.join(
        HOME if HOME is not None else "",
        ".config"))

CACHE_DIR = os.getenv("pygpm_CACHE_DIR", os.path.join(XDG_CACHE_DIR, "pygpm"))
CONFIG_DIR = os.path.join(XDG_CONFIG_DIR, "pygpm")
MODULE_DIR = os.path.dirname(__file__)

OS = platform.uname()[0]
