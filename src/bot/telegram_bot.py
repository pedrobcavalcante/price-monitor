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
from src.config.logging_config import get_logger
from src.infrastructure.telegram.application_provider import ApplicationProvider
from src.usecases.user_usecases import UserUseCases

logger = get_logger(__name__)


class TelegramBot:
    """Classe principal do bot Telegram com todas as funcionalidades."""

    def __init__(
        self,
        app_provider: ApplicationProvider,
        user_usecases: UserUseCases,
        start_handler: StartHandler,
        unknown_handler: UnknownHandler,
        message_handler: MessageHandler,
    ):
        """
        Inicializa o bot com as dependências injetadas.

        :param app_provider: Provedor da aplicação Telegram.
        :param user_usecases: Casos de uso relacionados ao usuário.
        :param start_handler: Handler para o comando /start.
        :param unknown_handler: Handler para comandos desconhecidos.
        :param message_handler: Handler para mensagens de texto.
        """
        self._app_provider = app_provider
        self._user_usecases = user_usecases
        self._start_handler = start_handler
        self._unknown_handler = unknown_handler
        self._message_handler = message_handler

    async def initialize(self) -> Application:
        """Inicializa a aplicação do bot e registra os handlers."""
        application = await self._app_provider.get_application()

        if not self._app_provider.is_initialized():
            raise RuntimeError("Falha ao inicializar a aplicação do bot")

        await self._register_handlers(application)
        return application

    async def _register_handlers(self, application: Application) -> None:
        """Registra todos os handlers na aplicação."""
        application.add_handler(CommandHandler("start", self._start_handler.handle))
        application.add_handler(
            TelegramMessageHandler(
                filters.TEXT & ~filters.COMMAND, self._message_handler.handle
            )
        )
        application.add_handler(
            TelegramMessageHandler(filters.COMMAND, self._unknown_handler.handle)
        )
        logger.info("Handlers registrados com sucesso.")

    def run(self) -> None:
        """Inicia o bot e mantém ele em execução."""
        try:
            # Cria loop assíncrono e obtém a aplicação
            loop = asyncio.get_event_loop()
            application = loop.run_until_complete(self.initialize())

            logger.info("Iniciando polling do bot...")
            # Inicia o polling - método bloqueante que mantém o bot rodando
            application.run_polling(drop_pending_updates=True)

        except Exception as e:
            logger.error(f"Erro ao executar o bot: {e}")
            raise
