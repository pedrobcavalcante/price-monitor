import logging
import sys
from datetime import datetime
from typing import Optional
import os

from src.config.settings import LOG_LEVEL, LOG_FORMAT


def configure_logging(module_name: Optional[str] = None) -> logging.Logger:
    """
    Configura o logging para a aplicação, capturando todos os logs do terminal.

    Args:
        module_name: Nome do módulo para personalizar o nome do arquivo de log
    """
    # Gera um nome de arquivo dinâmico com timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    prefix = f"{module_name}_" if module_name else ""
    log_filename = f"{prefix}log_{timestamp}.log"

    # Define o diretório de logs
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # Cria a pasta logs se não existir
    log_filepath = os.path.join(log_dir, log_filename)

    # Converte o nível de log de string para constante do logging
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)

    # Configura o handler para arquivo
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Configura o handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Configura o logger raiz para capturar todos os logs
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove handlers anteriores se existirem
    if root_logger.handlers:
        root_logger.handlers.clear()

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Captura também logs de bibliotecas externas
    for logger_name in ["telegram", "httpx"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

    # Retorna um logger específico se um nome de módulo for fornecido
    if module_name:
        return logging.getLogger(module_name)
    return root_logger


# Para uso em importação direta
def get_logger(name: str):
    """
    Obtém um logger configurado para o módulo especificado.

    Args:
        name: Nome do módulo (geralmente __name__)

    Returns:
        Logger configurado
    """
    # Se a configuração global já foi feita, apenas retorna o logger
    if logging.getLogger().handlers:
        return logging.getLogger(name)
    # Caso contrário, configura o logging e retorna
    return configure_logging(name)
