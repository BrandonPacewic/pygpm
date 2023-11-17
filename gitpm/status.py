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
    def index_next_t(start: int) -> int:
        return util.find_next(status, start, lambda x: x.startswith("\t"))

    try:
        status = util.read_command(["git", "status"])
    except Exception as e:
        util.colored_print(util.Colors.RED, f"Not a git repository: {e}")
        sys.exit(1)

    tokens: dict[str, Any] = {}
    for i, line in enumerate(status):
        if line.startswith("On branch"):
            tokens["on-branch"] = line[10:]

        elif line.startswith("Changes not staged for commit:"):
            tokens["untracked-changes"] = []
            for j in range(index_next_t(i), len(status)):
                if status[j].startswith("\t"):
                    tokens["untracked-changes"].append(
                        f"{status[j][13:].strip()}")
                else:
                    break

        elif line.startswith("Untracked files:"):
            tokens["untracked-files"] = []
            for j in range(index_next_t(i), len(status)):
                if status[j].startswith("\t"):
                    tokens["untracked-files"].append(status[j].strip())
                else:
                    break

        elif line.startswith("Changes to be committed:"):
            tokens["tracked-changes"] = []
            for j in range(index_next_t(i), len(status)):
                if status[j].startswith("\t"):
                    tokens["tracked-changes"].append(status[j].strip())
                else:
                    break

    return tokens


def print_status(config: Config) -> None:
    def get_token_length(token: str) -> int:
        try:
            return len(tokens[token])
        except KeyError:
            return 0

    def print_tokens(tokens: List[str]) -> None:
        for token in tokens:
            util.colored_print(status_color, f"  {token}")

    tokens = parse_git_status()
    assert "on-branch" in tokens

    status_color = get_status_color(tokens)
    print(f"Branch: {tokens['on-branch']}")

    not_staged_len = get_token_length("untracked-changes")
    if not_staged_len > 0 or (
        not_staged_len == 0 and config.get(
            "status",
            "always_list_clean") == "true"):
        print(
            f"Detected {not_staged_len} files with changes not"
            f" staged for commit{':' if not_staged_len > 0 else '.'}"
        )

        if "untracked-changes" in tokens:
            print_tokens(tokens["untracked-changes"])

    not_tracked_len = get_token_length("untracked-files")
    if not_tracked_len > 0 or (
        not_tracked_len == 0 and config.get(
            "status",
            "always_list_clean") == "true"):
        print(
            f"Detected {not_tracked_len} untracked files"
            f"{':' if not_tracked_len > 0 else '.'}"
        )

        if "untracked-files" in tokens:
            print_tokens(tokens["untracked-files"])

    staged_len = get_token_length("tracked-changes")
    if staged_len > 0 or (
        staged_len == 0 and config.get("status", "always_list_clean") == "true"
    ):
        print(
            f"Detected {staged_len} files staged for commit"
            f"{':' if staged_len > 0 else '.'}"
        )

        if "tracked-changes" in tokens:
            print_tokens(tokens["tracked-changes"])

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
