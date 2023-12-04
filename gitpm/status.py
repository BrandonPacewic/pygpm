"""Output the status of the current git repository or all repositories managed
by gitpm.
"""

# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import sys

from optparse import Values
from typing import Any

from gitpm.config import CONFIG
from gitpm.command import Command
from gitpm.util import read_command, is_git_repository
from gitpm.logging import Colors, get_logger

logger = get_logger(__name__)


class StatusCommand(Command):
    def add_options(self) -> None:
        # TODO
        pass

    def run(self, options: Values, args: list[str]) -> None:
        # TODO: Expand to all repositories managed by gitpm.
        if not is_git_repository():
            logger.colored_critical(Colors.BOLD_RED, "Not a git repository.")
            sys.exit(1)

        tokens = parse_git_status()
        assert "on-branch" in tokens

        logger.info(f"Branch: {tokens['on-branch']}")

        suggested_actions = False
        list_clean = CONFIG.get("status", "always_list_clean") == "true"

        if tokens["untracked-files"]:
            suggested_actions = True
            logger.info(
                f"Detected {len(tokens['untracked-files'])} untracked file(s):")
            logger.colored_info(Colors.RED, "\n".join(
                [f"\t{token}" for token in tokens["untracked-files"]]))
        elif list_clean:
            logger.info("No untracked files detected.")

        if tokens["untracked-changes"]:
            suggested_actions = True
            logger.info(
                f"Detected {len(tokens['untracked-changes'])} file(s) "
                "with changes not staged for commit:")
            logger.colored_info(Colors.YELLOW, "\n".join(
                [f"\t{token}" for token in tokens["untracked-changes"]]))
        elif list_clean:
            logger.info("No untracked changes detected.")

        if tokens["tracked-changes"]:
            suggested_actions = True
            logger.info(
                f"Detected {len(tokens['tracked-changes'])} file(s) "
                "staged for commit:")
            logger.colored_info(Colors.GREEN, "\n".join(
                [f"\t{token}" for token in tokens["tracked-changes"]]))
        elif list_clean:
            logger.info("No staged changes detected.")

        if suggested_actions:
            logger.colored_info(Colors.YELLOW, "Status: Actions Suggested")
        else:
            logger.colored_info(Colors.GREEN, "Status: Clean")


def parse_git_status() -> dict[str, Any]:
    status = read_command(["git", "status", "--branch", "--porcelain"])
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

    if tokens["untracked-files"] and (tokens["untracked-changes"]
                                      or tokens["tracked-changes"]):
        tokens["untracked-files"].append("")

    if tokens["untracked-changes"] and (tokens["tracked-changes"]
                                        or CONFIG.get("status", "always_list_clean") == "true"):
        tokens["untracked-changes"].append("")

    return tokens
