from argparse import ArgumentParser
from application.services.scraping_service import ScrapingService
from application.services.notification_service import NotificationService

def main():
    parser = ArgumentParser(description="OLX Price Monitor CLI")
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="URL of the OLX listing to monitor"
    )
    parser.add_argument(
        "--notify",
        action='store_true',
        help="Enable notifications for price changes"
    )
    
    args = parser.parse_args()

    scraping_service = ScrapingService()
    notification_service = NotificationService()

    print(f"Monitoring URL: {args.url}")
    
    if args.notify:
        print("Notifications are enabled.")
    
    # Start monitoring the specified URL
    scraping_service.monitor_url(args.url, notification_service)

if __name__ == "__main__":
    main()