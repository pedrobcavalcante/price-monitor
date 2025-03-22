from src.application.services.scraping_service import ScrapingService
from src.application.services.notification_service import NotificationService

def main():
    scraping_service = ScrapingService()
    notification_service = NotificationService()

    # Start monitoring for new postings and price changes
    scraping_service.monitor_products(notification_service)

if __name__ == "__main__":
    main()