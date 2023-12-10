# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
Output the status of the current git repository or all repositories managed
by pygpm.
"""

import sys
import os

from optparse import Values
from typing import Any

from pygpm.config import CONFIG
from pygpm.command import Command
from pygpm.util import read_command, is_git_repository, get_repository_cached_data
from pygpm.logging import Colors, get_logger

logger = get_logger(__name__)


class StatusCommand(Command):
    """
    Output status of current git repository or optionally list status of
    all git repositories actively being tracked by pygpm.
    """

    usage = """
      %prog [options]"""

    def add_options(self) -> None:
        self.cmd_options.add_option(
            "-a",
            "--list-all",
            action="store_true",
            dest="list_all",
            default=False,
            help="Force list status off all tracked repositories."
        )

        self.cmd_options.add_option(
            "--compact-all",
            action="store_true",
            dest="compact_all",
            default=False,
            help="Show a condensed version of 'pygpm status --list-all'."
        )

    # TODO: Fix branching?
    def run(self, options: Values, args: list[str]) -> None:
        if is_git_repository() and not options.list_all and not options.compact_all:
            tokens = parse_git_status()
            assert "on-branch" in tokens

            logger.info(f"Branch: {tokens['on-branch']}")

            suggested_actions = False
            list_clean = CONFIG.get("status", "always_list_clean") == "true"

            if tokens["untracked-files"]:
                suggested_actions = True
                logger.info(
                    f"Detected {len(tokens['untracked-files'])} untracked file(s):")
                tokens["untracked-files"].append("")
                logger.colored_info(Colors.RED, "\n".join(
                    [f"\t{token}" for token in tokens["untracked-files"]]))
            elif list_clean:
                logger.info("No untracked files detected.")

            if tokens["untracked-changes"]:
                suggested_actions = True
                logger.info(
                    f"Detected {len(tokens['untracked-changes'])} file(s) "
                    "with changes not staged for commit:")
                tokens["untracked-changes"].append("")
                logger.colored_info(Colors.YELLOW, "\n".join(
                    [f"\t{token}" for token in tokens["untracked-changes"]]))
            elif list_clean:
                logger.info("No untracked changes detected.")

            if tokens["tracked-changes"]:
                suggested_actions = True
                logger.info(
                    f"Detected {len(tokens['tracked-changes'])} file(s) "
                    "staged for commit:")
                tokens["tracked-changes"].append("")
                logger.colored_info(Colors.GREEN, "\n".join(
                    [f"\t{token}" for token in tokens["tracked-changes"]]))
            elif list_clean:
                logger.info("No staged changes detected.")

            if suggested_actions:
                logger.colored_info(Colors.YELLOW, "Status: Actions Suggested")
            else:
                logger.colored_info(Colors.GREEN, "Status: Clean")

            return

        repositories = get_repository_cached_data()

        if repositories is None:
            logger.colored_critical(
                Colors.BOLD_RED,
                "pygpm found no tracked repositories.")
            sys.exit(1)

        repository_status_tokens: dict[str, dict[str, Any]] = {}

        for name, info in repositories.items():
            repository_status_tokens[name] = parse_git_status(info["path"])

        # TODO: Add tabulate.
        if not options.compact_all:
            for name, info in repositories.items():
                logger.info(f"{name} - Author {info['author']}")


def parse_git_status(command_dir: str = os.getcwd()) -> dict[str, Any]:
    status = read_command("git status --porcelain --branch", command_dir)
    tokens: dict[str, Any] = {
        "on-branch": None,
        "untracked-changes": [],
        "untracked-files": [],
        "tracked-changes": [],
    }

    for line in status:
        if line.startswith("##"):
            tokens["on-branch"] = line.split("...")[0][3:]
        elif line.startswith(" M"):
            tokens["untracked-changes"].append(line[3:].strip())
        elif line.startswith("M ") or line.startswith("A "):
            tokens["tracked-changes"].append(line[3:].strip())
        elif line.startswith("??"):
            tokens["untracked-files"].append(line[3:].strip())

    return tokens
