class Product:
    def __init__(self, name: str, url: str, current_price: float):
        self.name = name
        self.url = url
        self.current_price = current_price

    def __repr__(self):
        return f"Product(name={self.name}, url={self.url}, current_price={self.current_price})"

    def update_price(self, new_price: float):
        self.current_price = new_price