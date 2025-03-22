from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    """Envia uma mensagem quando o comando /start é recebido."""
    update.message.reply_text('Olá! Eu sou um bot. Como posso ajudar você?')

def register_handlers(dispatcher) -> None:
    """Registra os manipuladores de comandos no dispatcher."""
    dispatcher.add_handler(CommandHandler("start", start))