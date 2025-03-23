import asyncio
import logging
from src.config.logging_config import configure_logging
from src.bot.telegram_bot import TelegramBot

# Configura o logging antes de qualquer operação
logger = configure_logging()


def main():
    """Função principal para iniciar a aplicação."""
    logger.info("Iniciando a aplicação de monitoramento de preços...")

    # Inicializa e executa o bot do Telegram
    bot = TelegramBot()
    asyncio.run(bot.initialize())
    bot.start()


if __name__ == "__main__":
    main()
