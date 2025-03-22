from bs4 import BeautifulSoup
import requests
from typing import List, Dict

class OLXScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def scrape_product_listings(self, query: str) -> List[Dict]:
        url = f"{self.base_url}/search?q={query}"
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        listings = []

        for item in soup.select('.item'):
            title = item.select_one('.item-title').get_text(strip=True)
            price = item.select_one('.item-price').get_text(strip=True)
            link = item.select_one('a')['href']
            listings.append({
                'title': title,
                'price': price,
                'link': link
            })

        return listings

    def scrape_price_changes(self, product_url: str) -> Dict:
        response = requests.get(product_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        price = soup.select_one('.price').get_text(strip=True)
        
        return {
            'url': product_url,
            'current_price': price
        }