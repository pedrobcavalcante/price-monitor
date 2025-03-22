from typing import List, Dict, Optional
from loguru import logger
from src.infrastructure.scraping.olx_scraper import OLXScraper
from domain.entities.product import Product
from domain.entities.price_history import PriceHistory

class ScrapingService:
    def __init__(self, scraper_type: str = "olx"):
        """
        Initialize the scraping service with the appropriate scraper
        
        Args:
            scraper_type: Type of scraper to use (default: "olx")
        """
        if scraper_type.lower() == "olx":
            self.scraper = OLXScraper()
        else:
            raise ValueError(f"Unsupported scraper type: {scraper_type}")
            
    def search_products(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Search for products using the configured scraper
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of product dictionaries
        """
        logger.info(f"Searching for products with query: {query}")
        return self.scraper.scrape_product_listings(query, max_results)
        
    def get_product_details(self, product_url: str) -> Dict:
        """
        Get detailed information about a specific product
        
        Args:
            product_url: URL of the product page
            
        Returns:
            Dictionary containing product details
        """
        logger.info(f"Getting details for product: {product_url}")
        return self.scraper.scrape_product_details(product_url)
        
    def monitor_products(self, notification_service=None, queries: List[str] = None, max_results: int = 20):
        """
        Monitor products for price changes
        
        Args:
            notification_service: Service to send notifications (optional)
            queries: List of search queries to monitor
            max_results: Maximum number of results per query
        """
        if not queries:
            queries = ["iphone", "notebook"]
            
        logger.info(f"Starting to monitor products for queries: {queries}")
        
        for query in queries:
            products = self.search_products(query, max_results)
            logger.info(f"Found {len(products)} products for query '{query}'")
            
            for product in products:
                logger.info(f"Product: {product['title']} - Price: {product['price']}")
                
                # Here you would typically:
                # 1. Check if the product exists in the database
                # 2. If it exists, check if the price has changed
                # 3. If price changed, send notification
                # 4. Otherwise, add the product to the database
                
                if notification_service:
                    notification_service.notify(
                        f"Product found: {product['title']} - Price: {product['price']}",
                        product['link']
                    )