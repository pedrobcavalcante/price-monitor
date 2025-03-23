from typing import Optional
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from src.config.settings import TELEGRAM_BOT_TOKEN
from src.usecases.user_usecases import UserUseCases
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class TelegramBot:
    """Classe principal do bot Telegram com todas as funcionalidades."""

    def __init__(self, user_usecases: UserUseCases = UserUseCases()):
        """Inicializa o bot com as configurações fornecidas."""
        if not TELEGRAM_BOT_TOKEN:
            raise ValueError("O token do bot Telegram não pode ser None ou vazio.")
        self._token: str = TELEGRAM_BOT_TOKEN
        if not self._token:
            raise ValueError("O token do bot Telegram não pode ser None ou vazio.")
        self._application: Optional[Application] = None

        self._user_usecases = user_usecases

    async def start_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Envia uma mensagem quando o comando /start é recebido."""
        if not update.message:
            logger.warning("Mensagem de atualização não encontrada.")
            return

        is_valid, user = await self._user_usecases.verify_telegram_user(update)

        if not is_valid:
            # Direciona o usuário para o registro
            success, message = await self._user_usecases.register_user(update)
            if success:
                await update.message.reply_text(
                    f"{message}\nBem-vindo ao bot de monitoramento de preços!"
                )
            else:
                await update.message.reply_text(
                    f"{message}\nPor favor, tente novamente mais tarde."
                )
            return

        first_name = user.first_name if user else "Usuário"
        await update.message.reply_text(
            f"Olá, {first_name}! Eu sou o seu bot de monitoramento de preços. Como posso ajudar?"
        )

    async def unknown_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Responde a comandos desconhecidos."""
        if update.message:
            await update.message.reply_text(
                "Desculpe, não entendi esse comando. Por favor, use um comando válido."
            )
        else:
            logger.warning("Mensagem de atualização não encontrada.")

    async def handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Processa todas as mensagens não-comando recebidas."""
        if not update.message:
            logger.warning("Mensagem de atualização não encontrada.")
            return

        is_valid, _ = await self._user_usecases.verify_telegram_user(update)
        if not is_valid:
            success, message = await self._user_usecases.register_user(update)
            if success:
                await update.message.reply_text(
                    f"{message}\nAgora você pode utilizar os comandos disponíveis."
                )
            else:
                await update.message.reply_text(
                    f"{message}\nPor favor, tente novamente mais tarde."
                )
            return

        await update.message.reply_text(
            "Recebi sua mensagem. Para usar o bot, por favor utilize os comandos disponíveis."
        )

    def register_handlers(self):
        """Registra todos os handlers de comandos e mensagens."""
        if not self._application:
            raise RuntimeError("A aplicação do bot não foi inicializada.")

        # Registra o handler para o comando /start
        self._application.add_handler(CommandHandler("start", self.start_command))

        # Registra o handler para mensagens de texto
        self._application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

        # Registra o handler para comandos desconhecidos (deve ser o último)
        self._application.add_handler(
            MessageHandler(filters.COMMAND, self.unknown_command)
        )

    async def initialize(self):
        """Inicializa a aplicação do bot."""
        logger.info("Inicializando o bot Telegram...")
        self._application = Application.builder().token(self._token).build()
        self.register_handlers()
        await self._application.initialize()
        logger.info("Bot Telegram inicializado com sucesso.")

    def start(self):
        """Inicia o bot e começa a escutar mensagens."""
        if not self._application:
            raise RuntimeError("A aplicação do bot não foi inicializada.")
        logger.info("Bot iniciado e escutando mensagens...")
        self._application.run_polling()


if __name__ == "__main__":
    import asyncio

    bot = TelegramBot()
    asyncio.run(bot.initialize())
    bot.start()
