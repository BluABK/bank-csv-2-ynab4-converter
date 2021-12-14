import os
from pathlib import Path
import sys

import globals
from csv_parsers.BasicParser import BasicParser

MY_PATH = Path(os.path.realpath(sys.argv[0]))
MY_NAME = MY_PATH.name


def show_help():
    print("Usage: {} <Bank-statement.csv>".format(MY_NAME))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    csv_path = sys.argv[1]

    my_parser = BasicParser(csv_path, auto_parse=True)

    for statement in my_parser.statements:
        print(statement)
        #print(currency2float(statement.amount))

