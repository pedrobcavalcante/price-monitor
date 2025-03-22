# Conteúdo do arquivo: /telegram-bot/telegram-bot/src/main.py

import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config.settings import load_env

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Envia uma mensagem quando o comando /start é recebido."""
    update.message.reply_text('Olá! Eu sou um bot. Como posso ajudar você?')

def main() -> None:
    """Inicia o bot e começa a ouvir mensagens."""
    load_env()  # Carrega as variáveis de ambiente do arquivo .env
    token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not token:
        logger.error("Token do bot não encontrado. Verifique o arquivo .env.")
        return

    updater = Updater(token)

    # Adiciona o manipulador para o comando /start
    updater.dispatcher.add_handler(CommandHandler("start", start))

    # Inicia o bot
    updater.start_polling()
    logger.info("Bot iniciado e ouvindo mensagens...")
    updater.idle()

if __name__ == '__main__':
    main()