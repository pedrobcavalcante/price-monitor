class PriceHistory:
    def __init__(self, product_id):
        self.product_id = product_id
        self.price_changes = []

    def add_price_change(self, price, timestamp):
        self.price_changes.append({'price': price, 'timestamp': timestamp})

    def get_price_changes(self):
        return self.price_changes

    def get_latest_price(self):
        if self.price_changes:
            return self.price_changes[-1]['price']
        return None

    def get_price_change_history(self):
        return self.price_changes