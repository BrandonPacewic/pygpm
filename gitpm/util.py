# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import os
import subprocess
import time

from typing import List

from .settings import OS

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'


def colored_print(color: str, text: str) -> None:
    print(f"{color}{text}{Colors.END}")


def multiline_colored_print(color: str, text: List[str]) -> None:
    for line in text:
        colored_print(color, line)


def multiline_print(text: List[str]) -> None:
    for line in text:
        print(line)


class Timer:
    def __init__(self):
        self.tics = [time.perf_counter()]

    def add_tic(self):
        self.tics.append(time.perf_counter())

    def get_elapsed(self):
        try:
            return str('{:.3f}'.format(self.tics[-1] - self.tics[-2]))
        except IndexError:
            print('Elapsed is null')
            exit()


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
