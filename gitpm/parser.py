"""Responsible for parsing all command line arguments and calling
associated commands.
"""

# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import sys
import optparse

from importlib import import_module
from collections import namedtuple
from typing import Optional

from gitpm.core import __version__

CommandInfo = namedtuple("CommandInfo", "module, function, description")

# Holds the module and function associated with each command. Helps avoid
# costly unnecessary imports.
commands_dict: dict[str, CommandInfo] = {
    "status": CommandInfo(
        "gitpm.status",
        "print_status",
        "Show an enhanced status of the current git repository or the "
        "status of all repositories currently tracked by gitpm."
    ),
}


def create_main_parser() -> optparse.OptionParser:
    parser = optparse.OptionParser(
        usage="\n\tgitpm <command> [options]",
        # TODO: Make a custom indented help formatter.
        # formatter=optparse.IndentedHelpFormatter(),
    )
    parser.version = __version__
    parser.description = "\n".join(
        [""] + [
            f"\t{command} {description}"
            for command, description in commands_dict.items()
        ]
    )

    return parser


def parse_command(args: list[str]) -> Optional[int]:
    parser = create_main_parser()
    general_options, command_args = parser.parse_args(args)

    # TODO: General options: version
    # if general_options.version:
    #     parser.print_version()
    #     sys.exit(0)

    if not command_args or (
            command_args[0] == "help" and len(command_args) == 1):
        parser.print_help()
        sys.exit(0)

    command = command_args[0]

    if command not in commands_dict:
        guess = get_similar_commands(command)
        msg = [f"gitpm: '{command}' is not a gitpm command. See 'gitpm help'."]

        if guess:
            msg.append(f"\nDid you mean '{guess}'?")

        print("\n".join(msg))
        sys.exit(1)

    # TODO: Command class
    module_path, function_name, _ = commands_dict[command]
    module = import_module(module_path)
    function = getattr(module, function_name)
    function()


def get_similar_commands(command: str) -> Optional[str]:
    from difflib import get_close_matches

    command = command.lower()
    close_commands = get_close_matches(command, commands_dict.keys())

    if close_commands:
        return close_commands[0]
    else:
        return None
