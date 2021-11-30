class BankStatement:
    date = None
    date2 = None
    raw_text = None
    amount = None
    balance_afterwards = None

    def __init__(self, date=None, date2=None, raw_text=None, amount=None, balance_afterwards=None):
        self.date = date
        self.date2 = date2
        self.raw_text = raw_text
        self.amount = amount
        self.balance_afterwards = balance_afterwards

    def parse_raw_text(self, unparsed_text=None):
        if unparsed_text is None:
            unparsed_text = self.raw_text

    def __repr__(self):
        return "<BankStatement: date={}, date2={}, raw_text={}, amount={}, balance_afterwards={}>".format(
            self.date,
            self.date2,
            self.raw_text,
            self.amount,
            self.balance_afterwards
        )
