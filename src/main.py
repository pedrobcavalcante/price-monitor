import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from src.config.settings import load_env

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem quando o comando /start é recebido."""
    await update.message.reply_text("Olá! Eu sou um bot. Como posso ajudar você?")


def main() -> None:
    """Inicia o bot e começa a ouvir mensagens."""
    load_env()  # Carrega as variáveis de ambiente do arquivo .env
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        logger.error("Token do bot não encontrado. Verifique o arquivo .env.")
        return

    # Cria a aplicação do bot
    application = Application.builder().token(token).build()

    # Adiciona o manipulador para o comando /start
    application.add_handler(CommandHandler("start", start))

    # Inicia o bot
    logger.info("Bot iniciado e ouvindo mensagens...")
    application.run_polling()


if __name__ == "__main__":
    main()
