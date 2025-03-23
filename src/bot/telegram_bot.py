from typing import Optional
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler as TelegramMessageHandler,
    filters,
)
from src.bot.handlers.start_handler import StartHandler
from src.bot.handlers.unknown_handler import UnknownHandler
from src.bot.handlers.message_handler import MessageHandler
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
        self._application: Optional[Application] = None
        self._user_usecases = user_usecases

        # Instancia os handlers
        self._start_handler = StartHandler(user_usecases)
        self._unknown_handler = UnknownHandler()
        self._message_handler = MessageHandler(user_usecases)

    async def _get_application(self) -> Application:
        """
        Verifica se a aplicação do bot está inicializada e inicializa caso necessário.

        Returns:
            Application: A instância da aplicação inicializada
        """
        if not self._application:
            await self.initialize()
        return self._application  # type: ignore

    async def register_handlers(self):
        """Registra todos os handlers de comandos e mensagens."""
        app = await self._get_application()

        app.add_handler(CommandHandler("start", self._start_handler.handle))
        app.add_handler(
            TelegramMessageHandler(
                filters.TEXT & ~filters.COMMAND, self._message_handler.handle
            )
        )
        app.add_handler(
            TelegramMessageHandler(filters.COMMAND, self._unknown_handler.handle)
        )

    async def initialize(self):
        """Inicializa a aplicação do bot."""
        if self._application:
            logger.info("Bot Telegram já está inicializado.")
            return

        logger.info("Inicializando o bot Telegram...")
        self._application = Application.builder().token(self._token).build()
        await self.register_handlers()
        await self._application.initialize()
        logger.info("Bot Telegram inicializado com sucesso.")

    async def start(self, use_webhook=False, webhook_url=None, webhook_port=8443):
        """
        Inicia o bot e começa a escutar mensagens.

        Args:
            use_webhook: Se True, utiliza webhook em vez de polling
            webhook_url: URL para o webhook (necessário se use_webhook=True)
            webhook_port: Porta para o webhook
        """
        app = await self._get_application()

        logger.info("Bot iniciado e escutando mensagens...")

        if use_webhook:
            if not webhook_url:
                raise ValueError("URL do webhook é necessária quando use_webhook=True")

            app.run_webhook(
                listen="0.0.0.0",
                port=webhook_port,
                url_path=self._token,
                webhook_url=f"{webhook_url}/{self._token}",
            )
        else:
            # Executa o run_polling
            app.run_polling()
