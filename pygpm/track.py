# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
Add new git repositories for pygpm to track.
"""

import sys
import configparser
import os

from optparse import Values
from typing import Any

from pygpm.command import Command
from pygpm.logging import Colors, get_logger
from pygpm.util import is_git_repository, cache_repo_data

logger = get_logger(__name__)


class TrackCommand(Command):
    """
    Add a repository to be tracked globally by pygpm.
    """

    usage = """
      %prog [options] <repository path> ...
      %prog [options] -a <repositories root path> ..."""

    def add_options(self) -> None:
        self.cmd_options.add_option(
            "-a",
            "--add-all",
            action="store_true",
            dest="add_all",
            default=False,
            help="Add all git repositories in child directories."
        )

    def run(self, options: Values, args: list[str]) -> None:
        if len(args) == 0:
            self.parser.print_help()
            sys.exit(1)

        if options.add_all:
            for arg in args:
                for dir in os.listdir(arg):
                    if os.path.isdir(dir) and is_git_repository(dir):
                        logger.debug(f"Caching {os.path.abspath(dir)}...")
                        make_and_cache_data(dir)
        else:
            for arg in args:
                arg = os.path.abspath(arg)

                if not os.path.isdir(arg):
                    logger.colored_critical(
                        Colors.BOLD_RED, f"{arg} is not a valid directory.")
                    sys.exit(1)
                elif not is_git_repository(arg):
                    logger.colored_critical(
                        Colors.BOLD_RED, f"{arg} is not a valid git repository.")
                    sys.exit(1)

                make_and_cache_data(arg)


def make_and_cache_data(dir: str) -> None:
    repo_dir = os.path.abspath(dir)
    data = extract_repository_data(repo_dir)
    cache_repo_data(**data)


def extract_repository_data(repo_dir: str) -> dict[str, Any]:
    git_config = configparser.ConfigParser()
    git_config.read(f"{repo_dir}/.git/config")
    url = git_config.get('remote "origin"', "url")
    data = {
        "name": repo_dir.split("/")[-1],
        "author": url.split(":")[-1].split("/")[0],
        "url": url,
        "path": repo_dir
    }

    return data
