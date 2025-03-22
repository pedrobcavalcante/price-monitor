from dataclasses import dataclass

@dataclass
class ProductDTO:
    name: str
    url: str
    current_price: float
    previous_price: float = None
    price_history: list = None

    def __post_init__(self):
        if self.price_history is None:
            self.price_history = []