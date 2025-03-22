import pytest
from src.infrastructure.scraping.olx_scraper import OLXScraper

@pytest.fixture
def olx_scraper():
    return OLXScraper()

def test_scrape_product_listings(olx_scraper):
    url = "https://sp.olx.com.br/sao-paulo-e-regiao/celulares?q=iphone"
    listings = olx_scraper.scrape_product_listings(url)
    assert isinstance(listings, list)
    assert len(listings) > 0

def test_scrape_product_details(olx_scraper):
    url = "https://sp.olx.com.br/sao-paulo-e-regiao/celulares?q=iphone"
    listings = olx_scraper.scrape_product_listings(url)
    product_url = listings[0]['url']
    product_details = olx_scraper.scrape_product_details(product_url)
    assert 'name' in product_details
    assert 'price' in product_details
    assert 'description' in product_details

def test_scrape_price_changes(olx_scraper):
    url = "https://sp.olx.com.br/sao-paulo-e-regiao/celulares?q=iphone"
    listings = olx_scraper.scrape_product_listings(url)
    product_url = listings[0]['url']
    initial_price = olx_scraper.scrape_product_details(product_url)['price']
    
    # Simulate a price change
    olx_scraper.simulate_price_change(product_url, new_price=1500)
    
    updated_price = olx_scraper.scrape_product_details(product_url)['price']
    assert updated_price == 1500
    assert updated_price != initial_price