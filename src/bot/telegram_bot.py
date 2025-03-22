import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("O token do bot não foi encontrado no arquivo .env")


# Função para responder ao comando /start
def start(update: Update, _) -> None:
    update.message.reply_text(
        "Olá! Eu sou o bot de monitoramento de preços. Como posso ajudar?"
    )


# Função para responder mensagens de texto
def echo(update: Update, _) -> None:
    update.message.reply_text(f"Você disse: {update.message.text}")


# Configuração principal do bot
def main():
    # Inicializar o bot com o token
    updater = Updater(BOT_TOKEN)

    # Obter o despachante para registrar os handlers
    dispatcher = updater.dispatcher

    # Registrar comandos e mensagens
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Iniciar o bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
