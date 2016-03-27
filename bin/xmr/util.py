import os
import configparser


def replace_last(s, old, new):
    return s[::-1].replace(old[::-1], new[::-1], 1)[::-1]


def read_config(config_file):

    if not os.path.isfile(config_file):
        print(config_file + ' not found, please create one.')
        return 1

    config = configparser.ConfigParser()

    config.read(config_file)

    return config['default']
