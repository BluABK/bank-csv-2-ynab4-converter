import csv
import os
from pathlib import Path
import sys
import json
import datetime

#MY_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
from bank_statement import BankStatement

MY_PATH = Path(os.path.realpath(sys.argv[0]))
MY_NAME = MY_PATH.name
CONFIG_PATH = MY_PATH.joinpath("config.json")

# Default config
CONFIG = {
    "csv_parser": {
        "encoding": "utf-8-sig",
        "reader_options": {
            "delimiter": ";"
        }
    }
}

# Override default config with custom config, if present. TODO: Make a loader, handle incomplete file/overrides
if os.path.isfile(CONFIG_PATH.absolute()):
    print("Loaded config file.")
    with open("config.json", "r") as config_file:
        CONFIG = json.load(config_file)


def show_help():
    print("Usage: {} <Bank-statement.csv>".format(MY_NAME))


def currency2float(s):
    """
    Takes a currency amount string and returns a computed float value.

    NB: If Unicode parsing is required in future replace the reverser with this grapheme based solution:
    https://stackoverflow.com/a/56282726
    :param s:
    :return:
    """
    past_delim = False
    is_negative = False
    characteristic_str_rev = ''
    mantissa_str_rev = ''

    # Read every char from end to start so that the order is mantissa --> delim --> characteristic --> whether negative
    for c in s[::-1]:
        if c.isdigit():
            if not past_delim:
                mantissa_str_rev += c
            else:
                characteristic_str_rev += c
        elif c == '-':
            is_negative = True
        else:
            # Delim can be ',', '.', ' ' or anything not a digit depending on your locale.
            past_delim = True

    # Undo reversion of characteristic and mantissa
    characteristic_str = "".join(characteristic_str_rev[::-1])
    mantissa_str = "".join(mantissa_str_rev[::-1])

    return float(('-' if is_negative else '') + characteristic_str + '.' + mantissa_str)


def parse(csv_path, reader_options=None, file_encoding=None):
    statements = []

    if reader_options is None:
        reader_options = CONFIG["csv_parser"]["reader_options"]
    if file_encoding is None:
        file_encoding = CONFIG["csv_parser"]["encoding"]

    with open(csv_path, 'r+', newline='', encoding=file_encoding) as csv_file:
        spamreader = csv.reader(csv_file, **reader_options)

        for row in spamreader:
            print("row: {}".format(row))
            statements.append(
                BankStatement(date=datetime.datetime.strptime(row[0], "%d.%m.%Y"),
                              date2=datetime.datetime.strptime(row[1], "%d.%m.%Y"),
                              raw_text=row[2],
                              amount=currency2float(row[3]),
                              balance_afterwards=currency2float(row[4]))
            )

    return statements


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    statements = parse(sys.argv[1])
    for statement in statements:
        print(statement)
        #print(currency2float(statement.amount))

