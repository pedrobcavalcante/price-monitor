from pathlib import Path
import os

class Settings:
    def __init__(self):
        self.OLX_BASE_URL = "https://sp.olx.com.br"
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///olx_price_monitor.db")
        self.NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL", "your_email@example.com")
        self.NOTIFICATION_API_KEY = os.getenv("NOTIFICATION_API_KEY", "your_api_key")
        self.SCRAPING_INTERVAL = int(os.getenv("SCRAPING_INTERVAL", 60))  # in seconds
        self.PRODUCTS_TO_MONITOR = [
            {"name": "iPhone", "url": f"{self.OLX_BASE_URL}/sao-paulo-e-regiao/celulares?q=iphone"},
            {"name": "Apartamento", "url": f"{self.OLX_BASE_URL}/sao-paulo-e-regiao/imoveis?q=apartamento"},
        ]

settings = Settings()