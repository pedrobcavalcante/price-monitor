class Price:
    def __init__(self, amount: float, currency: str = "BRL"):
        self.amount = amount
        self.currency = currency
        self.validate()

    def validate(self):
        if self.amount < 0:
            raise ValueError("Price amount cannot be negative.")
        if not isinstance(self.currency, str) or len(self.currency) != 3:
            raise ValueError("Currency must be a three-letter code.")

    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"

    def __eq__(self, other):
        if not isinstance(other, Price):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other):
        if not isinstance(other, Price):
            return NotImplemented
        return self.amount < other.amount

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __add__(self, other):
        if not isinstance(other, Price):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError("Cannot add prices with different currencies.")
        return Price(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        if not isinstance(other, Price):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError("Cannot subtract prices with different currencies.")
        return Price(self.amount - other.amount, self.currency)