import time
import json
from typing import List, Dict, Optional
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re


class VisualScraper:
    def __init__(self, base_url: str = "https://www.olx.com.br"):
        self.base_url = base_url
        self.driver = None

    def _initialize_driver(self):
        """Initialize Chrome driver with options to bypass SSL errors"""
        options = Options()
        # Options to fix SSL handshake errors
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-insecure-localhost")

        # Additional useful options
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Optional: Uncomment if you want to run headless
        # options.add_argument('--headless')

        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
            return driver
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {str(e)}")
            return None

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

    def scrape_olx_with_selenium(self, query: str, max_results: int = 20) -> List[Dict]:
        """Scrape OLX using Selenium to bypass SSL and other issues"""
        search_url = f"{self.base_url}/brasil?q={query.replace(' ', '+')}"
        logger.info(f"Abrindo URL no Chrome: {search_url}")

        self.driver = self._initialize_driver()
        if not self.driver:
            logger.error("Failed to initialize Chrome driver")
            return []

        try:
            # Load the page
            self.driver.get(search_url)

            # Wait for page to load completely
            time.sleep(10)

            # Extract listings from JSON data in the page
            json_data = None
            try:
                script_element = self.driver.find_element(By.ID, "__NEXT_DATA__")
                if script_element:
                    json_data = json.loads(script_element.get_attribute("textContent"))
                    ads_list = (
                        json_data.get("props", {}).get("pageProps", {}).get("ads", [])
                    )

                    if ads_list and isinstance(ads_list, list):
                        listings = []
                        for i, ad in enumerate(ads_list):
                            if i >= max_results:
                                break

                            try:
                                title = ad.get("subject", "Unknown Title")
                                price_text = ad.get("price", "R$ 0")
                                price_value = self.extract_price(price_text)
                                product_url = ad.get("url", "")
                                image_url = ad.get("thumbnail", None)

                                listings.append(
                                    {
                                        "title": title,
                                        "price": price_text,
                                        "price_value": price_value,
                                        "link": product_url,
                                        "image_url": image_url,
                                        "id": ad.get("listId"),
                                    }
                                )
                            except Exception as e:
                                logger.error(f"Error parsing ad from JSON: {str(e)}")

                        logger.info(f"Encontrados {len(listings)} anúncios no JSON")
                        return listings
            except Exception as e:
                logger.error(f"Error extracting JSON data with Selenium: {str(e)}")

            # Fallback to HTML scraping if JSON extraction failed
            logger.info("JSON extraction failed, falling back to HTML scraping")

            # Wait for product elements to be visible
            product_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "li.sc-1fcmfeb-2")
                )
            )[:max_results]

            listings = []
            for element in product_elements:
                try:
                    link_element = element.find_element(By.TAG_NAME, "a")
                    product_url = link_element.get_attribute("href")

                    title_element = element.find_element(By.TAG_NAME, "h2")
                    title = title_element.text if title_element else "Unknown Title"

                    price_element = element.find_element(
                        By.CSS_SELECTOR, "span.m7nrfa-0"
                    )
                    price_text = price_element.text if price_element else "R$ 0"
                    price_value = self.extract_price(price_text)

                    image_element = element.find_element(By.TAG_NAME, "img")
                    image_url = (
                        image_element.get_attribute("src") if image_element else None
                    )

                    # Extract ad ID from URL
                    ad_id = None
                    if product_url:
                        id_match = re.search(r"/(\d+)$", product_url)
                        if id_match:
                            ad_id = id_match.group(1)

                    listings.append(
                        {
                            "title": title,
                            "price": price_text,
                            "price_value": price_value,
                            "link": product_url,
                            "image_url": image_url,
                            "id": ad_id,
                        }
                    )
                except Exception as e:
                    logger.error(f"Error parsing product element: {str(e)}")

            logger.info(f"Encontrados {len(listings)} anúncios no HTML")
            return listings

        except Exception as e:
            logger.error(f"Error in visual scraping: {str(e)}")
            return []
        finally:
            # Close the browser
            if self.driver:
                self.driver.quit()
                self.driver = None
