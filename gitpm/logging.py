"""Customized logging for gitpm.
"""

# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import logging
import logging.config

from enum import Enum
from typing import Any, cast

Colors = Enum("Colors", ["GREEN", "RED", "BOLD_RED", "YELLOW", "END"])

COLOR_PAIRS: dict[Colors, str] = {
    Colors.GREEN: "\033[92m",
    Colors.RED: "\033[91m",
    Colors.BOLD_RED: "\033[1;91m",
    Colors.YELLOW: "\033[93m",
    Colors.END: "\033[0m",
}


class ColoredLogger(logging.Logger):
    def colored_log(
            self,
            verbosity: int,
            color: Colors,
            msg: str,
            *args: Any,
            **kwargs: Any) -> None:
        color_code = COLOR_PAIRS[color]
        color_end = COLOR_PAIRS[Colors.END]
        self.log(
            verbosity,
            f"{color_code}{msg}{color_end}",
            *args,
            **kwargs)

    def colored_debug(
            self,
            color: Colors,
            msg: str,
            *args: Any,
            **kwargs: Any) -> None:
        self.colored_log(logging.DEBUG, color, msg, *args, **kwargs)

    def colored_info(
            self,
            color: Colors,
            msg: str,
            *args: Any,
            **kwargs: Any) -> None:
        self.colored_log(logging.INFO, color, msg, *args, **kwargs)

    def colored_warning(
            self,
            color: Colors,
            msg: str,
            *args: Any,
            **kwargs: Any) -> None:
        self.colored_log(logging.WARNING, color, msg, *args, **kwargs)

    def colored_critical(
            self,
            color: Colors,
            msg: str,
            *args: Any,
            **kwargs: Any) -> None:
        self.colored_log(logging.CRITICAL, color, msg, *args, **kwargs)


class ColoredFormatter(logging.Formatter):
    def __init__(
            self,
            *args: Any,
            no_color: bool = False,
            add_timestamp: bool = False,
            **kwargs: Any) -> None:
        self.add_timestamp = add_timestamp
        super().__init__(*args, **kwargs)

    def format(self, record: logging.LogRecord) -> str:
        formatted = super().format(record)
        prefix = ""

        if self.add_timestamp:
            prefix = f"{self.formatTime(record)} "

        formatted = "".join(
            [prefix + line for line in formatted.splitlines(True)])
        return formatted


# TODO: Add a logging file
def setup_logging(
        verbosity: int = logging.NOTSET,
        no_color: bool = False) -> None:
    if verbosity >= 1:
        level_number = logging.DEBUG
    elif verbosity == -1:
        level_number = logging.WARNING
    elif verbosity == -2:
        level_number = logging.ERROR
    elif verbosity <= -3:
        level_number = logging.CRITICAL
    else:
        level_number = logging.INFO

    level = logging.getLevelName(level_number)

    log_streams = {
        "stdout": "ext://sys.stdout",
    }

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colored": {
                "()": ColoredFormatter,
                "format": "%(message)s",
            },
        },
        "handlers": {
            "default": {
                "level": level,
                "formatter": "colored",
                "class": "logging.StreamHandler",
                "stream": log_streams["stdout"],
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": level,
                "propagate": True,
            },
        }
    }

    logging.config.dictConfig(logging_config)


def init_logging() -> None:
    logging.setLoggerClass(ColoredLogger)


def get_logger(name: str) -> ColoredLogger:
    return cast(ColoredLogger, logging.getLogger(name))
