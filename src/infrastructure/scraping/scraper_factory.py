from .olx_scraper import OLXScraper

class ScraperFactory:
    @staticmethod
    def create_scraper(scraper_type: str, *args, **kwargs) -> OLXScraper:
        if scraper_type == "olx":
            return OLXScraper(*args, **kwargs)
        else:
            raise ValueError(f"Unknown scraper type: {scraper_type}")