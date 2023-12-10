# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import setuptools
import sys

try:
    import pygpm
except ImportError:
    print("Error importing pygpm.")
    sys.exit(1)

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

    # Remove folder icon from pypi package readme.
    long_description = f"#{long_description[20:]}"


def main() -> None:
    setuptools.setup(
        name="pygpm",
        version=pygpm.__version__,
        author="Brandon Pacewic",
        description="A GitHub repository manager",
        long_description_content_type="text/markdown",
        long_description=long_description,
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
