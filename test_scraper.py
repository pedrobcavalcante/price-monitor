from src.infrastructure.scraping.olx_scraper import OLXScraper


def main():
    # Create the scraper
    scraper = OLXScraper()

    # Test searching for products
    search_query = "iphone"
    print(f"Searching for: {search_query}")

    listings = scraper.scrape_product_listings(search_query, max_results=5)

    # Display results
    print(f"Found {len(listings)} products:")
    for i, product in enumerate(listings, 1):
        print(f"{i}. {product['title']}")
        print(f"   Price: {product['price']}")
        print(f"   URL: {product['link']}")
        print()

    # If we have results, test getting details for the first one
    if listings:
        first_product_url = listings[0]["link"]
        print(f"Getting details for: {first_product_url}")

        details = scraper.scrape_product_details(first_product_url)

        print("\nProduct Details:")
        for key, value in details.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
