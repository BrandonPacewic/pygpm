# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
Miscellaneous utility functions and classes for pygpm.
"""

import os
import sys
import subprocess
import time
import json

from typing import Any, List, Optional

from pygpm.core import CACHE_DIR, OS, __version__


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


def make_file(new_file: str) -> None:
    os.system(f"touch {new_file}")


def read_file_json(input_file: str) -> dict[str, dict[str, Any]]:
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.decoder.JSONDecodeError:
        return {}


def write_file_json(output_file: str, data: dict) -> None:
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def create_dir(directory: str) -> None:
    os.makedirs(directory, exist_ok=True)


def copy_file(input_file: str, output_file: str) -> None:
    if OS == "Windows":
        os.system(f"copy {input_file} {output_file}")
    else:
        os.system(f"cp {input_file} {output_file}")


def read_command(command: str, command_dir: str = os.getcwd()) -> List[str]:
    return subprocess.check_output(
        command.split(" "),
        cwd=command_dir).decode("utf-8").splitlines()


def is_git_repository(directory: str = os.getcwd()) -> bool:
    # TODO: Potential problem with checking the status of a repository not
    # on drive c on windows.
    while directory != ("C:\\" if OS == "Windows" else "/"):
        if ".git" in os.listdir(directory):
            return True

        directory = os.path.dirname(directory)

    return False


def get_pygpm_version() -> str:
    pygpm_pkg_dir = os.path.join(os.path.dirname(__file__), "..", "..")
    pygpm_pkg_dir = os.path.abspath(pygpm_pkg_dir)

    return f"pygpm {__version__} from {pygpm_pkg_dir} (python {get_python_major_minor_version()})"


def get_python_major_minor_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}"


REPO_CACHE_FILE = f"{CACHE_DIR}/repos.json"


def get_repository_cached_data() -> Optional[dict[str, dict[str, Any]]]:
    data = read_file_json(REPO_CACHE_FILE)

    if len(data):
        return data

    return None


def cache_repo_data(name: str, author: str, url: str, path: str) -> None:
    if not os.path.isfile(REPO_CACHE_FILE):
        create_dir(CACHE_DIR)
        make_file(REPO_CACHE_FILE)
        data = {}
    else:
        data = read_file_json(REPO_CACHE_FILE)

    data[name] = {"author": author, "url": url, "path": path}
    write_file_json(REPO_CACHE_FILE, data)


def clean_cached_data() -> None:
    if os.path.isfile(REPO_CACHE_FILE):
        with open(REPO_CACHE_FILE, "w", encoding="utf-8") as file:
            file.write("")
