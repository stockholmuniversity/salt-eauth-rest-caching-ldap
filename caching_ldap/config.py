#!/usr/bin/env python3
import configparser
import os

def load_config(config_file=None):
    config_file = config_file or os.environ.get('CONFIG_FILE', 'config.ini')

    config = configparser.ConfigParser()
    config.read(config_file)

    return config


config = load_config()
