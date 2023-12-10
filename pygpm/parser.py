# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
Utility for parsing command line arguments throughout pygpm.
"""

import shutil
import textwrap

from collections import namedtuple
from functools import partial
from optparse import IndentedHelpFormatter, Option, OptionGroup, OptionParser
from typing import Any, Callable, List

from pygpm.core import __version__

# General options
VERSION: Callable[..., Option] = partial(
    Option,
    "-v",
    "--version",
    dest="version",
    action="store_true",
    help="Show version number and exit."
)

VERBOSE: Callable[..., Option] = partial(
    Option,
    "-V",
    "--verbose",
    dest="verbose",
    action="count",
    default=0,
    help="Increases output. Option is additive but functionally is capped at 1."
)

QUIET: Callable[..., Option] = partial(
    Option,
    "-q",
    "--quiet",
    dest="quiet",
    action="count",
    default=0,
    help="Decreases output. Option is additive and can be used up to 3 times."
)

NO_COLOR: Callable[..., Option] = partial(
    Option,
    "--no-color",
    dest="no_color",
    action="store_true",
    default=False,
    help="Disables color output."
)

SHOW_TIME: Callable[..., Option] = partial(
    Option,
    "--show-time",
    dest="show_time",
    action="store_true",
    default=False,
    help="Show the message stamp in the log output."
)

TIME_COMMAND: Callable[..., Option] = partial(
    Option,
    "--time-command",
    dest="time_command",
    action="store_true",
    default=False,
    help="Adds a timer onto tho selected command and displays the total command runtime."
)

GENERAL_GROUP: List[Callable[..., Option]] = [
    VERSION,
    VERBOSE,
    QUIET,
    NO_COLOR,
    SHOW_TIME,
    TIME_COMMAND
]


def make_general_group(parser: OptionParser) -> OptionGroup:
    group = OptionGroup(parser, "General Options")
    for option in GENERAL_GROUP:
        group.add_option(option())

    return group


CommandInfo = namedtuple("CommandInfo", "module, class_name, summary")

# Holds the module and classes associated with each command. Helps avoid
# costly unnecessary imports as individual command imports are done at runtime.
COMMANDS_DICT: dict[str, CommandInfo] = {
    "status": CommandInfo(
        "pygpm.status",
        "StatusCommand",
        "Show an enhanced status of the current git repository or the "
        "status of all repositories currently tracked by pygpm."
    ),
    "track": CommandInfo(
        "pygpm.track",
        "TrackCommand",
        "Add new git repositories for pygpm to track."
    ),
    "clean": CommandInfo(
        "pygpm.clean",
        "CleanCommand",
        "Clean all data related to tracked repositories."
    ),
    "help": CommandInfo(
        "pygpm.help",
        "HelpCommand",
        "Display help information for commands."
    ),
    "list": CommandInfo(
        "pygpm.list",
        "ListCommand",
        "List out the directory of all tracked git repositories."
    )
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
            metavar = option.metavar or option.dest

            if metavar is not None:
                opts.append(f" <{metavar.lower()}>")

        return "".join(opts)

    def format_heading(self, heading: str) -> str:
        if heading == "General Options":
            return ""

        return f"{heading}:\n"

    def format_usage(self, usage: str) -> str:
        return f"\nUsage: {self.indent_lines(textwrap.dedent(usage), '  ')}\n"

    def format_description(self, description: str) -> str:
        if not description:
            return ""

        # If TRUE then we are outputting help for the main parser
        # else this help block is for a specific command.
        if hasattr(self.parser, "main"):
            label = "Commands"
        else:
            label = "Description"

        description = description.lstrip("\n")
        description = description.rstrip()
        description = self.indent_lines(textwrap.dedent(description), "  ")
        description = f"{label}:\n{description}\n"

        return description

    def format_epilog(self, epilog: str) -> str:
        if epilog:
            return epilog

        return ""

    def indent_lines(self, text: str, indent: str) -> str:
        lines = [f"{indent}{line}" for line in text.split("\n")]
        return "\n".join(lines)
