"""Miscellaneous utility functions and classes for gitpm.
"""

# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import os
import sys
import subprocess
import time

from typing import List

from gitpm.core import OS, __version__


class Timer:
    def __init__(self) -> None:
        self.tics = [time.perf_counter()]

    def add_tic(self) -> None:
        self.tics.append(time.perf_counter())

    def get_elapsed(self) -> str:
        try:
            return f"{self.tics[-1] - self.tics[-2]:.3f}"
        except IndexError:
            return "-0.000"


def read_file(input_file: str) -> List[str]:
    with open(input_file, "r") as file:
        return file.read().splitlines()


def create_dir(directory: str) -> None:
    os.makedirs(directory, exist_ok=True)


def copy_file(input_file: str, output_file: str) -> None:
    if OS == "Windows":
        os.system(f"copy {input_file} {output_file}")
    else:
        os.system(f"cp {input_file} {output_file}")


def read_command(command: List[str]) -> List[str]:
    return subprocess.check_output(command).decode("utf-8").splitlines()


def is_git_repository(directory: str = os.getcwd()) -> bool:
    while directory != ("C:\\" if OS == "Windows" else "/"):
        if ".git" in os.listdir(directory):
            return True

        directory = os.path.dirname(directory)

    return False


def get_gitpm_version() -> str:
    gitpm_pkg_dir = os.path.join(os.path.dirname(__file__), "..", "..")
    gitpm_pkg_dir = os.path.abspath(gitpm_pkg_dir)

    return f"gitpm {__version__} from {gitpm_pkg_dir} (python {get_python_major_minor_version()})"


def get_python_major_minor_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}"
