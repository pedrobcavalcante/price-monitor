from telegram import Update
from telegram.ext import ContextTypes
from src.config.logging_config import get_logger
from src.usecases.user_usecases import UserUseCases

logger = get_logger(__name__)


class StartHandler:
    """Classe responsável por lidar com o comando /start."""

    def __init__(self, user_usecases: UserUseCases):
        self._user_usecases = user_usecases

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Envia uma mensagem quando o comando /start é recebido."""
        if not update.message:
            logger.warning("Mensagem de atualização não encontrada.")
            return

        is_valid, user = await self._user_usecases.verify_telegram_user(update)

        if not is_valid:
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
