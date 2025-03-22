import re
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from loguru import logger


class OLXScraper:
    def __init__(self, base_url: str = "https://www.olx.com.br"):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def extract_price(self, price_text: str) -> float:
        """Extract numeric price from text like 'R$ 1.200,00'"""
        if not price_text:
            return 0.0

        # Remove currency symbol and non-numeric chars except decimal separator
        clean_price = re.sub(r"[^\d,.]", "", price_text)
        # Replace comma with dot for decimal separator
        clean_price = clean_price.replace(",", ".")

        try:
            return float(clean_price)
        except ValueError:
            logger.error(f"Could not parse price: {price_text}")
            return 0.0

    def scrape_product_listings(self, query: str, max_results: int = 20) -> List[Dict]:
        """Search for products on OLX using a query string"""
        search_url = f"{self.base_url}/brasil?q={query.replace(' ', '+')}"

        try:
            response = requests.get(search_url, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            listings = []

            # Current OLX structure uses li elements with specific class
            product_elements = soup.select("li.sc-1fcmfeb-2")[:max_results]

            for element in product_elements:
                try:
                    link_element = element.select_one("a")
                    if not link_element:
                        continue

                    product_url = link_element.get("href")

                    # Check if URL is absolute
                    if product_url and not product_url.startswith("http"):
                        product_url = f"https://www.olx.com.br{product_url}"

                    if product_url:
                        title_element = element.select_one("h2")
                        title = (
                            title_element.text.strip()
                            if title_element
                            else "Unknown Title"
                        )

                        price_element = element.select_one("span.m7nrfa-0")
                        price_text = (
                            price_element.text.strip() if price_element else "R$ 0"
                        )
                        price_value = self.extract_price(price_text)

                        image_element = element.select_one("img")
                        image_url = image_element.get("src") if image_element else None

                        listings.append(
                            {
                                "title": title,
                                "price": price_text,
                                "price_value": price_value,
                                "link": product_url,
                                "image_url": image_url,
                            }
                        )
                except Exception as e:
                    logger.error(f"Error parsing product element: {str(e)}")

            return listings

        except Exception as e:
            logger.error(f"Error searching for products with query '{query}': {str(e)}")
            return []

    def scrape_product_details(self, product_url: str) -> Dict:
        """Scrape detailed information about a specific product"""
        try:
            response = requests.get(product_url, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract product title
            title_element = soup.select_one("h1.ad__sc-45jt43-0")
            title = title_element.text.strip() if title_element else "Unknown Title"

            # Extract price
            price_element = soup.select_one("span.ad__sc-1wimjbb-0")
            price_text = price_element.text.strip() if price_element else "R$ 0"
            price_value = self.extract_price(price_text)

            # Extract description
            desc_element = soup.select_one("div.ad__sc-r1wl6v-0")
            description = desc_element.text.strip() if desc_element else None

            # Extract image URL
            image_element = soup.select_one("img.image__image")
            image_url = image_element.get("src") if image_element else None

            return {
                "url": product_url,
                "title": title,
                "current_price": price_text,
                "price_value": price_value,
                "description": description,
                "image_url": image_url,
            }

        except Exception as e:
            logger.error(f"Error scraping product {product_url}: {str(e)}")
            return {"url": product_url, "error": str(e)}
