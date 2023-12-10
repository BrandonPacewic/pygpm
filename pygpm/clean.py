# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
Clean all cached pygpm repository data.
"""

import logging

from optparse import Values

from pygpm.command import Command
from pygpm.logging import Colors, get_logger
from pygpm.util import clean_cached_data

logger = get_logger(__name__)


class CleanCommand(Command):
    """
    Clean all tracked repository data from pygpm's cache.
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
