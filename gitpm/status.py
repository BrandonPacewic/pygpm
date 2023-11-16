# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import sys

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
                util.find_next(status, i, lambda x: x.startswith("\t")),
                len(status)
            ):
                if status[j].startswith("\t"):
                    tokens["untracked-changes"].append(
                        f"{status[j][13:].strip()}"
                    )
                else:
                    break

        elif line.startswith("Untracked files:"):
            tokens["untracked-files"] = []
            for j in range(
                util.find_next(status, i, lambda x: x.startswith("\t")),
                len(status)
            ):
                if status[j].startswith("\t"):
                    tokens["untracked-files"].append(status[j].strip())
                else:
                    break

        elif line.startswith("Changes to be committed:"):
            tokens["tracked-changes"] = []
            for j in range(
                util.find_next(status, i, lambda x: x.startswith("\t")),
                len(status)
            ):
                if status[j].startswith("\t"):
                    tokens["tracked-changes"].append(status[j].strip())
                else:
                    break

    return tokens


# TODO: Clean branching
def print_status() -> None:
    tokens = parse_git_status()
    assert "on-branch" in tokens

    status_color = get_status_color(tokens)
    print(f"Branch: {tokens['on-branch']}")

    if "untracked-changes" in tokens:
        not_staged_len = len(tokens["untracked-changes"])
    else:
        not_staged_len = 0

    print(
        f"Detected {not_staged_len} files with changes not"
        f" staged for commit{':' if not_staged_len > 0 else '.'}"
    )

    if not_staged_len > 0:
        util.multiline_colored_print(
            status_color,
            [f"  {token}" for token in tokens["untracked-changes"]]
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
        print()

    if "tracked-changes" in tokens:
        staged_len = len(tokens["tracked-changes"])
    else:
        staged_len = 0

    print(
        f"Detected {staged_len} files staged for commit"
        f"{':' if staged_len > 0 else '.'}"
    )

    if staged_len > 0:
        util.multiline_colored_print(
            status_color,
            [f"  {token}" for token in tokens["tracked-changes"]]
        )

    if status_color == util.Colors.GREEN:
        util.colored_print(status_color, "Status: Clean")
    elif status_color == util.Colors.YELLOW:
        util.colored_print(status_color, "\nStatus: Actions Suggested")
    else:
        # Will eventually be able to detect upstream changes and determine
        # if there are any conflicts.
        util.colored_print(status_color, "Status: Unknown")


def get_status_color(tokens: dict) -> str:
    if "untracked-changes" in tokens or \
       "untracked-files" in tokens or \
       "tracked-changes" in tokens:
        return util.Colors.YELLOW

    return util.Colors.GREEN
