import asyncio
from src.config.logging_config import configure_logging
from src.bot.telegram_bot import TelegramBot

# Configura o logging antes de qualquer operação
logger = configure_logging()


async def main():
    """Função principal para iniciar a aplicação."""
    logger.info("Iniciando a aplicação")

    # Inicializa e executa o bot do Telegram
    bot = TelegramBot()
    await bot.initialize()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
