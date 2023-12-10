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


def main() -> None:
    setuptools.setup(
        name="gitpm",
        version=VERSION,
        author="Brandon Pacewic",
        description="A git repository manager",
        long_description_content_type="text/markdown",
        long_description=LONG_DESCRIPTION,
        license="MIT",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License"
        ],
        url="https://github.com/BrandonPacewic/gitpm",
        packages=["gitpm"],
        entry_points={
            "console_scripts": [
                "gitpm=gitpm.__main__:main"
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
