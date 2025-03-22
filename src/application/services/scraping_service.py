from typing import List
from infrastructure.scraping.olx_scraper import OLXScraper
from domain.entities.product import Product
from domain.entities.price_history import PriceHistory

class ScrapingService:
    def __init__(self, scraper: OLXScraper):
        self.scraper = scraper

    def scrape_products(self, urls: List[str]) -> List[Product]:
        products = []
        for url in urls:
            product_data = self.scraper.scrape(url)
            product = Product(name=product_data['name'], url=url, current_price=product_data['price'])
            products.append(product)
        return products

    def track_price_changes(self, product: Product) -> PriceHistory:
        price_history = PriceHistory(product=product)
        current_price = self.scraper.get_current_price(product.url)
        price_history.add_price(current_price)
        return price_history