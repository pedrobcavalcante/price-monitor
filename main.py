from src.config.logging_config import configure_logging
from src.bot.telegram_bot import TelegramBot

# Configura o logging antes de qualquer operação
logger = configure_logging()

if __name__ == "__main__":
    logger.info("Iniciando a aplicação")

    # Criar e executar o bot
    # Este método fará toda a inicialização e então bloqueará para manter o bot rodando
    bot = TelegramBot()
    bot.run()
