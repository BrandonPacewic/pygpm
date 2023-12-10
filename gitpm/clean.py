# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
Clean all cached gitpm repository data.
"""

import logging

from optparse import Values

from gitpm.command import Command
from gitpm.logging import Colors, get_logger
from gitpm.util import clean_cached_data

logger = get_logger(__name__)


class CleanCommand(Command):
    """
    Clean all tracked repository data from gitpm's cache.
    """

    usage = """
      %prog [options]"""

    def run(self, options: Values, args: list[str]) -> None:
        if logger.getEffectiveLevel() <= logging.INFO:
            confirm = input(
                "This will clear all tracked repository cached data\n"
                "Are you sure you want to proceed? (y/n) "
            ).lower()
        else:
            confirm = input().lower()

        if confirm == "y":
            clean_cached_data()
            logger.info("Cleaned cached repository data.")
        else:
            logger.colored_info(Colors.RED, "Aborting.")
