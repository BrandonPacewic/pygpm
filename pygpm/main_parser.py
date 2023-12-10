# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
Functions for parsing the main pygpm command line arguments.
"""

import logging
import sys

from difflib import get_close_matches
from importlib import import_module
from optparse import OptionParser
from typing import Any, List, Optional, Tuple

from pygpm.command import Command
from pygpm.core import __version__
from pygpm.parser import COMMANDS_DICT, CustomIndentedHelpFormatter, make_general_group
from pygpm.util import get_pygpm_version

logger = logging.getLogger(__name__)


def create_main_parser() -> OptionParser:
    parser = OptionParser(
        usage="\n\tpygpm <command> [options]",
        add_help_option=False,  # Added manually.
        prog="pygpm",
        formatter=CustomIndentedHelpFormatter(),
    )
    parser.disable_interspersed_args()

    general_options = make_general_group(parser)
    parser.add_option_group(general_options)

    parser.main = True
    parser.version = get_pygpm_version()

    parser.description = "\n".join(
        [""] + [
            f"\t{command} {info.summary}"
            for command, info in COMMANDS_DICT.items()
        ]
    )

    return parser


def parse_command(args: list[str]) -> Tuple[str, List[str]]:
    parser = create_main_parser()

    # NOTE: Parser calls `disable_interspersed_args()`, so the result
    # will look like this:
    #  args: ['--nocolor', 'status', '--help']
    #  general_options: ['--nocolor']
    #  command_args: ['status', '--help']
    general_options, command_args = parser.parse_args(args)

    if general_options.version:
        parser.print_version()
        sys.exit(0)

    if not command_args or (
            command_args[0] == "help" and len(command_args) == 1):
        parser.print_help()
        sys.exit(0)

    command = command_args[0]

    if command not in COMMANDS_DICT:
        msg = [f"Unknown command '{command}'."]
        guess = get_similar_commands(command)

        if guess:
            msg.append(f"Did you mean '{guess}'?")

        logger.critical("\n\n".join(msg))
        sys.exit(1)

    command_args.remove(command)

    return command, command_args


def create_command(name: str, **kwargs: Any) -> Command:
    module_path, class_name, summary = COMMANDS_DICT[name]
    module = import_module(module_path)
    command_class = getattr(module, class_name)
    command = command_class(name, summary, **kwargs)

    return command


def get_similar_commands(command: str) -> Optional[str]:
    command = command.lower()
    close_commands = get_close_matches(command, COMMANDS_DICT.keys())

    if close_commands:
        return close_commands[0]

    return None
