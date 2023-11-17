"""
Output the status of the current git repository or all repositories managed
by gitpm.
"""

# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import sys

from typing import Any, List

from .config import Config
from . import util


def parse_git_status() -> dict:
    try:
        status = util.read_command(["git", "status"])
    except Exception as e:
        util.colored_print(util.Colors.RED, f"Not a git repository: {e}")
        sys.exit(1)

    tokens = {}
    for i, line in enumerate(status):
        if line.startswith("On branch"):
            tokens["on-branch"] = line[10:]

        elif line.startswith("Changes not staged for commit:"):
            tokens["untracked-changes"] = []
            for j in range(
                    util.find_next(
                        status,
                        i,
                        lambda x: x.startswith("\t")),
                    len(status)):
                if status[j].startswith("\t"):
                    tokens["untracked-changes"].append(
                        f"{status[j][13:].strip()}")
                else:
                    break

        elif line.startswith("Untracked files:"):
            tokens["untracked-files"] = []
            for j in range(
                    util.find_next(
                        status,
                        i,
                        lambda x: x.startswith("\t")),
                    len(status)):
                if status[j].startswith("\t"):
                    tokens["untracked-files"].append(status[j].strip())
                else:
                    break

        elif line.startswith("Changes to be committed:"):
            tokens["tracked-changes"] = []
            for j in range(
                    util.find_next(
                        status,
                        i,
                        lambda x: x.startswith("\t")),
                    len(status)):
                if status[j].startswith("\t"):
                    tokens["tracked-changes"].append(status[j].strip())
                else:
                    break

    return tokens


# TODO: Clean branching
def print_status(config: Config) -> None:
    def token_length(tokens: dict[str, List[Any]], token: str) -> int:
        try:
            return len(tokens[token])
        except KeyError:
            return 0

    tokens = parse_git_status()
    assert "on-branch" in tokens

    status_color = get_status_color(tokens)
    print(f"Branch: {tokens['on-branch']}")

    not_staged_len = token_length(tokens, "untracked-changes")
    if not_staged_len > 0 or (
        not_staged_len == 0 and config.get(
            "status",
            "always_list_clean") == "true"):
        print(
            f"Detected {not_staged_len} files with changes not"
            f" staged for commit{':' if not_staged_len > 0 else '.'}"
        )

        try:
            util.multiline_colored_print(
                status_color,
                [f"  {token}" for token in tokens["untracked-changes"]],
                True,
            )
        except KeyError:
            pass

    not_tracked_len = token_length(tokens, "untracked-files")
    if not_tracked_len > 0 or (
        not_tracked_len == 0 and config.get(
            "status",
            "always_list_clean") == "true"):
        print(
            f"Detected {not_tracked_len} untracked files"
            f"{':' if not_tracked_len > 0 else '.'}"
        )

        try:
            util.multiline_colored_print(
                status_color,
                [f"  {token}" for token in tokens["untracked-files"]],
                True,
            )
        except KeyError:
            pass

    staged_len = token_length(tokens, "tracked-changes")
    if staged_len > 0 or (
        staged_len == 0 and config.get("status", "always_list_clean") == "true"
    ):
        print(
            f"Detected {staged_len} files staged for commit"
            f"{':' if staged_len > 0 else '.'}"
        )

        try:
            util.multiline_colored_print(
                status_color,
                [f"  {token}" for token in tokens["tracked-changes"]],
                True,
            )
        except KeyError:
            pass

    if status_color == util.Colors.GREEN:
        util.colored_print(status_color, "Status: Clean")
    elif status_color == util.Colors.YELLOW:
        if "tracked-changes" not in tokens and config.get(
                "status", "always_list_clean") == "true":
            print()

        util.colored_print(status_color, "Status: Actions Suggested")
    else:
        # Will eventually be able to detect upstream changes and determine
        # if there are any conflicts.
        util.colored_print(status_color, "Status: Unknown")


def get_status_color(tokens: dict) -> str:
    if (
        "untracked-changes" in tokens
        or "untracked-files" in tokens
        or "tracked-changes" in tokens
    ):
        return util.Colors.YELLOW

    return util.Colors.GREEN
