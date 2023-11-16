# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import argparse
import sys

from .settings import __version__, CACHE_DIR, CONFIG_DIR
from .config import Config
from . import status

def get_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--version",
                        action="version", version=f"gitpm {__version__}")

    parser.add_argument("action", nargs="+", help="Action to perform")

    return parser


def parse_args(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    action = args.action[0]

    if action == "status":
        status.print_status()

    else:
        parser.print_help()
        sys.exit(1)


def main():
    config = Config()

    parser = get_args()
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    action = args.action[0]

    if action == "status":
        status.print_status()


if __name__ == "__main__":
    main()
