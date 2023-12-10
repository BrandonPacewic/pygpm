# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
List out the directory of all tracked git repositories.
"""

import sys

from optparse import Values

from pygpm.command import Command
from pygpm.logging import Colors, get_logger
from pygpm.util import get_repository_cached_data

logger = get_logger(__name__)


class ListCommand(Command):
    """
    List out the directory of all repositories tracked globally by pygpm.
    """

    usage = """
      %prog [options]"""

    def add_options(self) -> None:
        self.cmd_options.add_option(
            "--count",
            action="store_true",
            dest="count",
            default=False,
            help="Simply display the total number of tracked repositories."
        )

    def run(self, options: Values, args: list[str]) -> None:
        data = get_repository_cached_data()

        if data is None:
            logger.colored_critical(
                Colors.BOLD_RED,
                "pygpm found no tracked repositories.")
            sys.exit(1)

        if options.count:
            logger.info(
                f"There are currently {len(data)} repositories tracked by pygpm.")
        else:
            for name, info in data.items():
                logger.info(f"{name}: {info['path']}")
