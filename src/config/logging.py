import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("olx_price_monitor.log"),
            logging.StreamHandler()
        ]
    )

setup_logging()