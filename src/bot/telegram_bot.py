import asyncio
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
from src.infrastructure.telegram.application_provider import ApplicationProvider

logger = get_logger(__name__)


class TelegramBot:
    """Classe principal do bot Telegram com todas as funcionalidades."""

    def __init__(self, user_usecases: UserUseCases = UserUseCases()):
        """Inicializa o bot com as configurações fornecidas."""
        if not TELEGRAM_BOT_TOKEN:
            raise ValueError("O token do bot Telegram não pode ser None ou vazio.")

        self._app_provider = ApplicationProvider(TELEGRAM_BOT_TOKEN)
        self._user_usecases = user_usecases

        # Inicializa os handlers diretamente
        self._start_handler = StartHandler(user_usecases)
        self._unknown_handler = UnknownHandler()
        self._message_handler = MessageHandler(user_usecases)

    async def initialize(self) -> Application:
        """Inicializa a aplicação do bot e registra os handlers."""
        application = await self._app_provider.get_application()

        if not self._app_provider.is_initialized():
            raise RuntimeError("Falha ao inicializar a aplicação do bot")

        await self._register_handlers(application)
        return application

    async def _register_handlers(self, application: Application) -> None:
        """Registra todos os handlers na aplicação."""
        # Registra handler do comando start
        application.add_handler(CommandHandler("start", self._start_handler.handle))

        # Registra handler para mensagens de texto que não são comandos
        application.add_handler(
            TelegramMessageHandler(
                filters.TEXT & ~filters.COMMAND, self._message_handler.handle
            )
        )

        # Registra handler para comandos desconhecidos
        application.add_handler(
            TelegramMessageHandler(filters.COMMAND, self._unknown_handler.handle)
        )

        logger.info("Handlers registrados com sucesso.")

    async def start(self) -> Application:
        """Inicializa o bot e retorna a aplicação pronta para uso."""
        application = await self.initialize()
        logger.info("Bot inicializado e pronto para escutar mensagens.")
        return application

    def run(self) -> None:
        """Inicia o bot e mantém ele em execução."""
        try:
            # Configura um novo loop de eventos
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Obtém a aplicação e inicia o polling
            application = loop.run_until_complete(self.initialize())
            logger.info("Iniciando polling do bot...")
            application.run_polling()
        except Exception as e:
            logger.error(f"Erro ao executar o bot: {e}")
            raise
