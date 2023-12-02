"""Base command class for all gitpm commands.
"""

# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

from optparse import OptionParser, OptionGroup, Values
from typing import List, Tuple

from gitpm.parser import CustomIndentedHelpFormatter, make_general_group
from gitpm.logging import setup_logging


class Command:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        self.parser = OptionParser(
            prog=f"gitpm {self.name}",
            description=self.description,
            formatter=CustomIndentedHelpFormatter(),
            add_help_option=False,
        )

        option_group_name = f"{self.name} Options"
        self.cmd_options = OptionGroup(self.parser, option_group_name)

        general_options = make_general_group(self.parser)
        self.parser.add_option_group(general_options)

        self.add_options()

    def add_options(self) -> None:
        pass

    def run(self, options: Values, args: list[str]) -> None:
        raise NotImplementedError

    def parse(self, args: list[str]) -> Tuple[Values, List[str]]:
        return self.parser.parse_args(args)

    def main(self, args: list[str]) -> None:
        options, args = self.parse(args)

        self.verbosity = options.verbose - options.quiet

        setup_logging(self.verbosity, options.no_color)

        self.run(options, args)
