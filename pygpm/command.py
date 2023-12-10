# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
Base command class for all pygpm commands.
"""

import logging

from optparse import OptionParser, OptionGroup, Values
from typing import List, Tuple

from pygpm.parser import CustomIndentedHelpFormatter, make_general_group
from pygpm.logging import Colors, setup_logging, get_logger
from pygpm.util import Timer

logger = get_logger(__name__)


class Command:
    # TODO: Move usage to init?
    usage: str = ""

    def __init__(self, name: str, summary: str) -> None:
        self.name = name
        self.summary = summary
        self.verbosity = logging.INFO

        self.parser = OptionParser(
            prog=f"pygpm {self.name}",
            usage=self.usage,
            description=self.__doc__,
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

        setup_logging(self.verbosity, options.no_color, options.show_time)

        if options.time_command:
            command_timer = Timer()

        self.run(options, args)

        if options.time_command:
            command_timer.add_tic()
            logger.colored_info(Colors.YELLOW,
                                f"Run time: {command_timer.get_elapsed()}s")
