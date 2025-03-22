from typing import List
from src.domain.entities.product import Product

class ProductRepository:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def get_all_products(self) -> List[Product]:
        return self.products

    def find_product_by_url(self, url: str) -> Product:
        for product in self.products:
            if product.url == url:
                return product
        return None

    def update_product(self, updated_product: Product) -> None:
        for index, product in enumerate(self.products):
            if product.url == updated_product.url:
                self.products[index] = updated_product
                break