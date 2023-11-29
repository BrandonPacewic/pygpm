"""Responsible for parsing all command line arguments and calling
associated commands.
"""

# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import sys
import shutil
import textwrap

from collections import namedtuple
from importlib import import_module
from functools import partial
from optparse import IndentedHelpFormatter, Option, OptionGroup, OptionParser
from typing import Any, Callable, Optional, List

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


class CustomIndentedHelpFormatter(IndentedHelpFormatter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["max_help_position"] = 30
        kwargs["indent_increment"] = 1
        kwargs["width"] = shutil.get_terminal_size()[0] - 2
        super().__init__(*args, **kwargs)

    def format_option_strings(self, option: Option) -> str:
        opts = []

        if option._short_opts:
            opts.append(option._short_opts[0])

        if option._long_opts:
            opts.append(option._long_opts[0])

        if len(opts) > 1:
            opts.insert(1, ", ")

        if option.takes_value():
            metavar = option.metavar or option.dest.lower()
            opts.append(f" <{metavar.lower()}>")

        return "".join(opts)

    def format_heading(self, heading: str) -> str:
        if heading == "General Options":
            return ""

        return f"{heading}:\n"

    def format_usage(self, usage: str) -> str:
        return f"\nUsage: {self.indent_lines(textwrap.dedent(usage), ' ')}\n"

    def format_description(self, description: str) -> str:
        if not description:
            return ""

        description = description.lstrip("\n")
        description = description.rstrip()
        description = self.indent_lines(textwrap.dedent(description), "  ")
        description = f"Commands:\n{description}\n"

        return description

    def format_epilog(self, epilog: str) -> str:
        if epilog:
            return epilog

        return ""

    def indent_lines(self, text: str, indent: str) -> str:
        lines = [indent + line for line in text.splitlines()]
        return "\n".join(lines)


def create_main_parser() -> OptionParser:
    parser = OptionParser(
        usage="\n\tgitpm <command> [options]",
        add_help_option=False,  # Added manually.
        prog="gitpm",
        formatter=CustomIndentedHelpFormatter(),
    )
    parser.disable_interspersed_args()

    general_options = make_general_group(parser)
    parser.add_option_group(general_options)

    parser.main = True
    parser.version = __version__

    parser.description = "\n".join(
        [""] + [
            f"\t{command} {info.description}"
            for command, info in COMMANDS_DICT.items()
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
