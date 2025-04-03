from typing import Optional
from telegram.ext import Application
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class ApplicationProvider:
    """Responsável por gerenciar a aplicação do Telegram Bot."""

    def __init__(self, token: str):
        """Inicializa o provedor com o token do bot."""
        self._token = token
        self._application: Optional[Application] = None

    async def get_application(self) -> Application:
        """Retorna a instância da aplicação, inicializando-a se necessário."""
        if not self._application:
            self._application = Application.builder().token(self._token).build()
            await self._application.initialize()
            logger.info("Aplicação do bot inicializada com sucesso.")
        return self._application

    def is_initialized(self) -> bool:
        """Verifica se a aplicação já foi inicializada."""
        return self._application is not None
