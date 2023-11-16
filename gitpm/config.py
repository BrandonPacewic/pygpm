# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import configparser
import os

from .settings import CONFIG_DIR, MODULE_DIR
from . import util

def create_default_config() -> None:
    util.create_dir(CONFIG_DIR)
    util.copy_file(
        os.path.join(MODULE_DIR, "config/default.ini"),
        os.path.join(CONFIG_DIR, "config.ini")
    )


class Config:
    def __init__(self) -> None:
        self.config_path = os.path.join(CONFIG_DIR, "config.ini")

        if not os.path.isfile(self.config_path):
            create_default_config()

        self.config = configparser.ConfigParser()
        self.load()
            
    def load(self) -> None:
        self.config.read_dict({
            "gitpm": {
                "auto_refresh_on_dir_change": "false",
            }
        })

        self.config.read(self.config_path)

    def get(self, section: str, option: str) -> str:
        return self.config.get(section, option)
