import csv
import datetime

from bank_statement import BankStatement
from handlers.config_handler import CONFIG
from utils import currency2float


class BasicParser:
    csv_path = None
    reader_options = None
    file_encoding = None
    statements = []

    def __init__(self, csv_path, reader_options=None, file_encoding=None, auto_parse=True):
        """
        Basic Bank Statement CSV Parser.

        Will parse each separate field, but won't delve into deciphering additional fields from description etc.

        For that, use an advanced parser instead.

        :param csv_path:
        :param reader_options:
        :param file_encoding:
        :param auto_parse:
        """
        self.csv_path = csv_path

        self.reader_options = CONFIG["csv_parser"]["reader_options"] if reader_options is None else reader_options
        self.file_encoding = CONFIG["csv_parser"]["encoding"] if file_encoding is None else file_encoding

        if auto_parse:
            self.parse()

    def parse(self, csv_path=None, reader_options=None, file_encoding=None):
        self.statements = []

        if csv_path is None:
            csv_path = self.csv_path
        if reader_options is None:
            reader_options = self.reader_options
        if file_encoding is None:
            file_encoding = self.file_encoding

        with open(csv_path, 'r+', newline='', encoding=file_encoding) as csv_file:
            spamreader = csv.reader(csv_file, **reader_options)

            for row in spamreader:
                # print("row: {}".format(row))
                self.statements.append(
                    BankStatement(date=datetime.datetime.strptime(row[0], "%d.%m.%Y"),
                                  date2=datetime.datetime.strptime(row[1], "%d.%m.%Y"),
                                  raw_text=row[2],
                                  amount=currency2float(row[3]),
                                  balance_afterwards=currency2float(row[4]))
                )

        return self.statements
