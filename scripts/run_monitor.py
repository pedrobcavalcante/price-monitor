from src.application.services.scraping_service import ScrapingService
from src.application.services.notification_service import NotificationService
import os
from loguru import logger

def main():
    """
    Main function to run the price monitor
    """
    # Configure logger
    logger.info("Starting OLX Price Monitor")
    
    # Initialize services
    scraping_service = ScrapingService(scraper_type="olx")
    
    # Create a simple notification service (without email for now)
    notification_service = NotificationService()
    
    # Define queries to monitor
    queries = ["iphone", "macbook", "ps5"]
    
    # Start monitoring
    logger.info(f"Monitoring products for queries: {queries}")
    scraping_service.monitor_products(
        notification_service=notification_service,
        queries=queries,
        max_results=10
    )
    
    logger.info("Monitoring complete")

if __name__ == "__main__":
    main()
