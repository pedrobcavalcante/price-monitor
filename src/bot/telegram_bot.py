from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os
from dotenv import load_dotenv
import logging

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Função que trata o comando /start
def start(update: Update, context: CallbackContext) -> None:
    """Envia uma mensagem quando o comando /start é recebido."""
    update.message.reply_text('Olá! Eu sou o seu bot. Como posso ajudar?')

def main() -> None:
    """Inicia o bot."""
    # Cria o Updater e passa o token do bot
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    updater = Updater(token)

    # Obtém o dispatcher para registrar os manipuladores
    dispatcher = updater.dispatcher

    # Registra o manipulador para o comando /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Inicia o bot
    updater.start_polling()

    # Executa o bot até que o usuário pressione Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()