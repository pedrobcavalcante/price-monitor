import time
import json
import os
import subprocess
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
        # Add more aggressive options to ignore SSL errors
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-insecure-localhost")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Set SSL protocol version
        options.add_argument("--ssl-version-max=tls1.3")
        options.add_argument("--ssl-version-min=tls1.2")

        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
            logger.info("Chrome driver initialized successfully")
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

    def scroll_page(self, scroll_count=3, scroll_pause_time=2):
        """Scroll down the page a few times with pauses"""
        if not self.driver:
            logger.error("Driver not initialized, cannot scroll")
            return

        try:
            for i in range(scroll_count):
                # Execute JavaScript to scroll down
                self.driver.execute_script("window.scrollBy(0, 800);")
                logger.info(f"Scrolled down {i+1}/{scroll_count}")
                # Pause to allow page to load
                time.sleep(scroll_pause_time)
        except Exception as e:
            logger.error(f"Error scrolling the page: {str(e)}")

    def save_and_open_results(self, listings: List[Dict], query: str):
        """Save scraping results to a text file and open it"""
        if not listings:
            logger.warning("No results to save")
            return

        # Create a formatted string with the results
        current_time = time.strftime("%Y%m%d-%H%M%S")
        filename = f"olx_search_{query.replace(' ', '_')}_{current_time}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"OLX Search Results for '{query}' - {len(listings)} items found\n")
            f.write("=" * 80 + "\n\n")

            for i, item in enumerate(listings, 1):
                f.write(f"{i}. {item.get('title', 'Unknown Title')}\n")
                f.write(f"   Price: {item.get('price', 'N/A')}\n")
                f.write(f"   Link: {item.get('link', 'N/A')}\n")
                if item.get("image_url"):
                    f.write(f"   Image: {item.get('image_url')}\n")
                f.write(f"   ID: {item.get('id', 'N/A')}\n")
                f.write("\n")

        # Open the file with the default application
        try:
            if os.name == "nt":  # Windows
                os.startfile(filename)
            elif os.name == "posix":  # Linux, Mac
                subprocess.call(("xdg-open", filename))

            logger.info(f"Results saved to {filename} and opened")
        except Exception as e:
            logger.error(f"Error opening the results file: {str(e)}")
            logger.info(f"Results saved to {filename}")

    def scrape_olx_with_selenium(self, query: str, max_results: int = 20) -> List[Dict]:
        """Scrape OLX using Selenium to bypass SSL and other issues"""
        search_url = f"{self.base_url}/brasil?q={query.replace(' ', '+')}"
        logger.info(f"Abrindo URL no Chrome: {search_url}")

        self.driver = self._initialize_driver()
        if not self.driver:
            logger.error("Failed to initialize Chrome driver")
            return []

        try:
            # Load the page with retry logic for SSL errors
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    self.driver.get(search_url)
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Attempt {attempt+1} failed, retrying: {str(e)}"
                        )
                        time.sleep(5)
                    else:
                        raise

            # Wait for page to load completely
            time.sleep(10)

            # Scroll down to load more content
            self.scroll_page()

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

                        # Save and open the results
                        self.save_and_open_results(listings, query)

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

            # Save and open the results
            self.save_and_open_results(listings, query)

            return listings

        except Exception as e:
            logger.error(f"Error in visual scraping: {str(e)}")
            return []
        finally:
            # Close the browser
            if self.driver:
                self.driver.quit()
                self.driver = None
