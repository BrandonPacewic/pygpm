# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import argparse
import os
import sys

from gitpm.core import __version__
from gitpm.config import Config
from gitpm.status import print_status
from gitpm.util import Colors, colored_print, is_git_repository


def get_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v", "--version", action="version", version=f"gitpm {__version__}"
    )

    parser.add_argument("action", nargs="+", help="Action to perform")

    return parser


def main() -> None:
    config = Config()

    parser = get_args()
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    action = args.action[0]

    if action == "status":
        if not is_git_repository(os.getcwd()):
            colored_print(Colors.RED, "Not a git repository.")
            sys.exit(1)

        print_status(config)


if __name__ == "__main__":
    main()
