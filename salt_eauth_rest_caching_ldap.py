#!/usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-function-docstring

from su.logging import console, logging, structured


def main():
    logger = logging.getLogger("myapp")
    logger.setLevel(logging.INFO)
    logger.info("My INFO message")


if __name__ == "main":
    main()
