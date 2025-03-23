import os
from pathlib import Path
from dotenv import load_dotenv

# Define o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(BASE_DIR / ".env")

# Configurações do bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configurações de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = BASE_DIR / "logs" / "app.log"

# Garante que o diretório de logs existe
LOG_FILE.parent.mkdir(exist_ok=True)

# Validação de configurações críticas
if not TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "Token do Telegram não encontrado. Configure a variável TELEGRAM_BOT_TOKEN no arquivo .env"
    )


class Config:
    """Classe de configuração para o bot Telegram."""

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

    @staticmethod
    def validate():
        """Valida se as configurações necessárias estão presentes."""
        if not Config.TELEGRAM_TOKEN:
            raise ValueError("A variável de ambiente TELEGRAM_TOKEN não está definida.")
