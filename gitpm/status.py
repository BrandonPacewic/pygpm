# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import sys

from . import util

def print_status() -> None:
    try:
        status = util.read_command(["git", "status"])
    except:
        util.colored_print(util.Colors.RED, "Not a git repository")
        sys.exit(1)

    tokens = {}

    for i, line in enumerate(status):
        if line.startswith("On branch"):
            tokens["on-branch"] = line[10:]

        elif line.startswith("Changes not staged for commit:"):
            tokens["changes-not-staged-for-commit"] = []
            for j in range(i + 3, len(status)):
                if status[j].startswith("\t"):
                    tokens["changes-not-staged-for-commit"].append(
                        f"{status[j][13:].strip()}"
                    )
                else:
                    break

        elif line.startswith("Untracked files:"):
            tokens["untracked-files"] = []
            for j in range(i + 2, len(status)):
                if status[j].startswith("\t"):
                    tokens["untracked-files"].append(status[j].strip())
                else:
                    break

    assert("on-branch" in tokens)

    status_color = get_status_color(tokens)
    print(f"Branch: {tokens['on-branch']}")

    if "changes-not-staged-for-commit" in tokens:
        not_staged_len = len(tokens["changes-not-staged-for-commit"])
    else:
        not_staged_len = 0

    print(
        f"Detected {not_staged_len} files with changes not"
        f" staged for commit{':' if not_staged_len > 0 else '.'}"
    )

    if not_staged_len > 0:
        util.multiline_colored_print(
            status_color, 
            [f"  {token}" for token in tokens["changes-not-staged-for-commit"]]
        )
        print()

    if "untracked-files" in tokens:
        not_tracked_len = len(tokens["untracked-files"])
    else:
        not_tracked_len = 0

    print(
        f"Detected {not_tracked_len} untracked files"
        f"{':' if not_tracked_len > 0 else '.'}"
    )

    if not_tracked_len > 0:
        util.multiline_colored_print(
            status_color,
            [f"  {token}" for token in tokens["untracked-files"]]
        )

    if status_color == util.Colors.GREEN:
        util.colored_print(status_color, "Status: Clean")
    elif status_color == util.Colors.YELLOW:
        util.colored_print(status_color, "\nStatus: Uncommitted changes")
    else:
        # Will eventually be able to detect upstream changes and determine
        # if there are any conflicts.
        util.colored_print(status_color, "Status: Unknown")


def get_status_color(tokens: dict) -> str:
    if "changes-not-staged-for-commit" in tokens or "untracked-files" in tokens:
        return util.Colors.YELLOW

    return util.Colors.GREEN
