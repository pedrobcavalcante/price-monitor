import logging
import sys
from src.config.settings import LOG_LEVEL, LOG_FORMAT, LOG_FILE


def configure_logging():
    """Configura o logging para a aplicação, capturando todos os logs do terminal."""
    # Converte o nível de log de string para constante do logging
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)

    # Configura o handler para arquivo
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Configura o handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Configura o logger raiz para capturar todos os logs
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Captura também logs de bibliotecas externas
    for logger_name in ["telegram", "httpx"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

    return root_logger


# Chama a função de configuração de logging ao importar o módulo
configure_logging()
