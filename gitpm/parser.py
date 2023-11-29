"""Responsible for parsing all command line arguments and calling
associated commands.
"""

# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import sys

from collections import namedtuple
from importlib import import_module
from functools import partial
from optparse import Option, OptionGroup, OptionParser
from typing import Callable, Optional, List

from gitpm.core import __version__

# General options
VERSION: Callable[..., Option] = partial(
    Option,
    "-v",
    "--version",
    dest="version",
    action="store_true",
    help="Show version number and exit."
)

GENERAL_GROUP: List[Callable[..., Option]] = [
    VERSION,
]


def make_general_group(parser: OptionParser) -> OptionGroup:
    group = OptionGroup(parser, "General Options")
    for option in GENERAL_GROUP:
        group.add_option(option())

    return group


CommandInfo = namedtuple("CommandInfo", "module, function, description")

# Holds the module and function associated with each command. Helps avoid
# costly unnecessary imports.
COMMANDS_DICT: dict[str, CommandInfo] = {
    "status": CommandInfo(
        "gitpm.status",
        "print_status",
        "Show an enhanced status of the current git repository or the "
        "status of all repositories currently tracked by gitpm."
    ),
}


def create_main_parser() -> OptionParser:
    parser = OptionParser(
        usage="\n\tgitpm <command> [options]",
        add_help_option=False,  # Added manually.
        prog="gitpm",
        # TODO: Make a custom indented help formatter.
        # formatter=optparse.IndentedHelpFormatter(),
    )
    parser.disable_interspersed_args()

    general_options = make_general_group(parser)
    parser.add_option_group(general_options)

    parser.main = True
    parser.version = __version__

    parser.description = "\n".join(
        [""] + [
            f"\t{command} {description}"
            for command, description in COMMANDS_DICT.items()
        ]
    )

    return parser


def parse_command(args: list[str]) -> Optional[int]:
    parser = create_main_parser()

    # NOTE: Parser calls `disable_interspersed_args()`, so the result
    # will look like this:
    #  args: ['--nocolor', 'status', '--help']
    #  general_options: ['--nocolor']
    #  command_args: ['status', '--help']
    general_options, command_args = parser.parse_args(args)

    if general_options.version:
        # TODO: Better print
        parser.print_version()
        sys.exit(0)

    if not command_args or (
            command_args[0] == "help" and len(command_args) == 1):
        parser.print_help()
        sys.exit(0)

    command = command_args[0]

    # Suggest possibly intended command.
    # TODO: Better print
    if command not in COMMANDS_DICT:
        guess = get_similar_commands(command)
        msg = [f"gitpm: '{command}' is not a gitpm command. See 'gitpm help'."]

        if guess:
            msg.append(f"\nDid you mean '{guess}'?")

        print("\n".join(msg))
        sys.exit(1)

    # TODO: Command class
    module_path, function_name, _ = COMMANDS_DICT[command]
    module = import_module(module_path)
    function = getattr(module, function_name)
    function()


def get_similar_commands(command: str) -> Optional[str]:
    from difflib import get_close_matches

    command = command.lower()
    close_commands = get_close_matches(command, COMMANDS_DICT.keys())

    if close_commands:
        return close_commands[0]
    else:
        return None
