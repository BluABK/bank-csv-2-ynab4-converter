import json
import os

import globals
import utils

PROJECT_PATH = globals.PROJECT_PATH

CONFIG_PATH = PROJECT_PATH.joinpath("config.json")

# Default config
CONFIG = {
    "csv_parser": {
        "parser": "basic",
        "encoding": "utf-8-sig",
        "reader_options": {
            "delimiter": ";"
        }
    }
}


# Override default config with custom config, if present.
if os.path.isfile(CONFIG_PATH.absolute()):
    print("Loaded config file.")
    with open("config.json", "r") as config_file:
        utils.update_nested_dict(CONFIG, json.load(config_file))
