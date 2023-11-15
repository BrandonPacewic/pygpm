# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import setuptools
import sys

try:
    import gitpm
except ImportError:
    print("Error importing gitpm.")
    sys.exit(1)

LONG_DESCRIPTION = open("README.md").read()
VERSION = gitpm.__version__

setuptools.setup(
    name="gitpm",
    version=VERSION,
    author="Brandon Pacewic",
    description="A git repository manager",
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    license="MIT",
    url="https://github.com/BrandonPacewic/gitpm",
    packages=["gitpm"],
    entry_points={"console_scripts": ["gitpm=gitpm.__main__:main"]},
    python_requires=">=3.6",
)
