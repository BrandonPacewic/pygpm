# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import setuptools
import sys

try:
    import pygpm
except ImportError:
    print("Error importing pygpm.")
    sys.exit(1)

LONG_DESCRIPTION = open("README.md").read()
VERSION = pygpm.__version__


def main() -> None:
    setuptools.setup(
        name="pygpm",
        version=VERSION,
        author="Brandon Pacewic",
        description="A GitHub repository manager",
        long_description_content_type="text/markdown",
        long_description=LONG_DESCRIPTION,
        license="MIT",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License"
        ],
        url="https://github.com/BrandonPacewic/pygpm",
        packages=["pygpm"],
        entry_points={
            "console_scripts": [
                "gpm=pygpm.__main__:main"
            ]
        },
        python_requires=">=3.9",
        extras_require={
            "git": ["git"],
            "github cli": ["gh"],
            "linting": [
                "pylint",
                "mypy",
            ],
        },
        include_package_data=True,
    )


if __name__ == "__main__":
    main()
