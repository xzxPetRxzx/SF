class APIException(Exception):
    pass

class Convert(self, base, quote, amount):
    def __init__(self):
        self.base = base
        self.quote = quote
        self.amount = amount

    def ask_price(self):
        pass

    def get_price(self):
        return ask_price(self.base, self.quote) * self.amount
