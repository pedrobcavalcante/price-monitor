from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Classe de configuração para o bot Telegram."""
    
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    @staticmethod
    def validate():
        """Valida se as configurações necessárias estão presentes."""
        if not Config.TELEGRAM_TOKEN:
            raise ValueError("A variável de ambiente TELEGRAM_TOKEN não está definida.")