"""Output the status of the current git repository or all repositories managed
by gitpm.
"""

# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

from typing import Any, List

from gitpm.config import CONFIG
from gitpm.util import Colors, colored_print, read_command, is_git_repository


def parse_git_status() -> dict[str, Any]:
    status = read_command(["git", "status", "--branch", "--porcelain"])
    tokens: dict[str, Any] = {}

    for i, line in enumerate(status):
        if line.startswith("##"):
            tokens["on-branch"] = line.split("...")[0][3:]

        elif line.startswith(" M"):
            tokens["untracked-changes"] = []
            for j in range(i - 1, len(status)):
                if status[j].startswith(" M"):
                    tokens["untracked-changes"].append(status[j][3:].strip())
                else:
                    break

        elif line.startswith("??"):
            tokens["untracked-files"] = []
            for j in range(i - 1, len(status)):
                if status[j].startswith("??"):
                    tokens["untracked-files"].append(status[j][3:].strip())
                else:
                    break

        elif line.startswith("M "):
            tokens["tracked-changes"] = []
            for j in range(i - 1, len(status)):
                if status[j].startswith("M "):
                    tokens["tracked-changes"].append(status[j][3:].strip())
                else:
                    break

    return tokens


def print_status() -> None:
    def get_token_length(token: str) -> int:
        if token in tokens:
            return len(tokens[token])

        return 0

    def print_tokens(tokens: List[str]) -> None:
        for token in tokens:
            colored_print(status_color, f"  {token}")

    if not is_git_repository():
        colored_print(Colors.RED, "Not a git repository.")
        return

    tokens = parse_git_status()
    assert "on-branch" in tokens

    status_color = get_status_color(tokens)
    print(f"Branch: {tokens['on-branch']}")

    list_clean = CONFIG.get("status", "always_list_clean") == "true"
    not_staged_len = get_token_length("untracked-changes")

    if not_staged_len > 0 or (not_staged_len == 0 and list_clean):
        print(
            f"Detected {not_staged_len} files with changes not"
            f" staged for commit{':' if not_staged_len > 0 else '.'}"
        )

        if "untracked-changes" in tokens:
            print_tokens(tokens["untracked-changes"])

    not_tracked_len = get_token_length("untracked-files")

    if not_tracked_len > 0 or (not_tracked_len == 0 and list_clean):
        print(
            f"Detected {not_tracked_len} untracked files"
            f"{':' if not_tracked_len > 0 else '.'}"
        )

        if "untracked-files" in tokens:
            print_tokens(tokens["untracked-files"])

    staged_len = get_token_length("tracked-changes")

    if staged_len > 0 or (staged_len == 0 and list_clean):
        print(
            f"Detected {staged_len} files staged for commit"
            f"{':' if staged_len > 0 else '.'}"
        )

        if "tracked-changes" in tokens:
            print_tokens(tokens["tracked-changes"])

    if status_color == Colors.GREEN:
        colored_print(status_color, "Status: Clean")
    elif status_color == Colors.YELLOW:
        if "tracked-changes" not in tokens and list_clean:
            print()

        colored_print(status_color, "Status: Actions Suggested")
    else:
        # Will eventually be able to detect upstream changes and determine
        # if there are any conflicts.
        colored_print(status_color, "Status: Unknown")


def get_status_color(tokens: dict) -> str:
    if (
        "untracked-changes" in tokens
        or "untracked-files" in tokens
        or "tracked-changes" in tokens
    ):
        return Colors.YELLOW

    return Colors.GREEN
