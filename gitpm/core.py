# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import os
import platform

__version__ = "0.1"

HOME = os.getenv("HOME", os.getenv("USERPROFILE"))
XDG_CACHE_DIR = os.getenv("XDG_CACHE_HOME", os.path.join(HOME, ".cache"))
XDG_CONFIG_DIR = os.getenv("XDG_CONFIG_HOME", os.path.join(HOME, ".config"))

CACHE_DIR = os.getenv("GITPM_CACHE_DIR", os.path.join(XDG_CACHE_DIR, "gitpm"))
CONFIG_DIR = os.path.join(XDG_CONFIG_DIR, "gitpm")
MODULE_DIR = os.path.dirname(__file__)

OS = platform.uname()[0]
