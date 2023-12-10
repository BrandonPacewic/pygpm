# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
Holds all configurable options for pygpm.
"""

import configparser
import os

from pygpm.core import CONFIG_DIR, MODULE_DIR
from pygpm.util import create_dir, copy_file

# TODO: Remove module
# TODO: Move string to pygpm/config/default.ini
"""
Config values for pygpm:

  status:
    always_list_clean:
      if 'true', 'pygpm status' will list categories even if they are empty
      example:
        Branch: main
        Detected 0 files with changes not staged for commit.
        Detected 0 untracked files.
        Detected 0 files staged for commit.
        Status: clean
      vs.
        Branch: main
        Status: clean
"""
CONFIG_DICT: dict[str, dict[str, str]] = {
    "status": {
        "always_list_clean": "true",
    }
}


def create_default_config() -> None:
    create_dir(CONFIG_DIR)
    copy_file(
        os.path.join(MODULE_DIR, "config/default.ini"),
        os.path.join(CONFIG_DIR, "config.ini"),
    )


class Config:
    def __init__(self) -> None:
        self.config_path = os.path.join(CONFIG_DIR, "config.ini")

        if not os.path.isfile(self.config_path):
            create_default_config()

        self.config = configparser.ConfigParser()
        self._load()

    def _load(self) -> None:
        self.config.read_dict(CONFIG_DICT)
        self.config.read(self.config_path)

    def get(self, section: str, option: str) -> str:
        return self.config.get(section, option)


CONFIG = Config()
