from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
import logging

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Função que trata o comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem quando o comando /start é recebido."""
    if update.message:
        await update.message.reply_text("Olá! Eu sou o seu bot. Como posso ajudar?")


async def main() -> None:
    """Inicia o bot."""
    # Cria a aplicação e passa o token do bot
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("The TELEGRAM_BOT_TOKEN environment variable is not set.")
    application = Application.builder().token(token).build()

    # Registra o manipulador para o comando /start
    application.add_handler(CommandHandler("start", start))

    # Inicia o bot
    await application.initialize()
    application.run_polling()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
