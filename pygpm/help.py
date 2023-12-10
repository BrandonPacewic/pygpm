# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
Shows usage and help information for pygpm commands.
"""

import sys

from optparse import Values
from typing import List

from pygpm.command import Command
from pygpm.parser import COMMANDS_DICT
from pygpm.main_parser import create_command, get_similar_commands
from pygpm.logging import get_logger

logger = get_logger(__name__)


class HelpCommand(Command):
    """
    Output help information for a specific command.
    """

    usage = """
      %prog [options] <pygpm command>"""

    def run(self, options: Values, args: List[str]) -> None:
        command_name = args[0]

        if command_name not in COMMANDS_DICT:
            msg = [f"Unknown command '{command_name}'."]
            guess = get_similar_commands(command_name)

            if guess:
                msg.append(f"Did you mean '{guess}'?")

            logger.critical("\n\n".join(msg))
            sys.exit(1)

        command = create_command(command_name)
        command.parser.print_help()
