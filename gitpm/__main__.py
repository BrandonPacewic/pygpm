# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import sys

from typing import List

from gitpm.core import __version__
from gitpm.parser import parse_command


def main(args: List[str]=sys.argv[1:]) -> None:
    parse_command(args)


if __name__ == "__main__":
    main()
