import logging
from datetime import datetime
from typing import Optional
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from src.config.settings import TELEGRAM_BOT_TOKEN

# Configuração do logger para incluir o momento de execução no nome do log
log_filename = f"telegram_bot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


class TelegramBot:
    """Classe principal do bot Telegram com todas as funcionalidades."""

    def __init__(self):
        """Inicializa o bot com as configurações fornecidas."""
        if not TELEGRAM_BOT_TOKEN:
            raise ValueError("O token do bot Telegram não pode ser None ou vazio.")
        self.token: str = (
            TELEGRAM_BOT_TOKEN  # Garantir que o token seja sempre uma string
        )
        if not self.token:
            raise ValueError("O token do bot Telegram não pode ser None ou vazio.")
        self.application: Optional[Application] = (
            None  # Tipagem explícita para Application
        )

    async def start_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Envia uma mensagem quando o comando /start é recebido."""
        if update.message:
            await update.message.reply_text(
                "Olá! Eu sou o seu bot de monitoramento de preços. Como posso ajudar?"
            )
        else:
            logger.warning("Mensagem de atualização não encontrada.")

    def register_handlers(self):
        """Registra todos os handlers de comandos e mensagens."""
        if not self.application:
            raise RuntimeError("A aplicação do bot não foi inicializada.")
        self.application.add_handler(CommandHandler("start", self.start_command))
        # Adicione outros handlers aqui conforme necessário

    async def initialize(self):
        """Inicializa a aplicação do bot."""
        logger.info("Inicializando o bot Telegram...")
        self.application = Application.builder().token(self.token).build()
        self.register_handlers()
        await self.application.initialize()
        logger.info("Bot Telegram inicializado com sucesso.")

    def start(self):
        """Inicia o bot e começa a escutar mensagens."""
        if not self.application:
            raise RuntimeError("A aplicação do bot não foi inicializada.")
        logger.info("Bot iniciado e escutando mensagens...")
        self.application.run_polling()


if __name__ == "__main__":
    import asyncio

    bot = TelegramBot()
    asyncio.run(bot.initialize())
    bot.start()
