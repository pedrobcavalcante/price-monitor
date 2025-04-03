from telegram import Update
from telegram.ext import ContextTypes
from src.config.logging_config import get_logger
from src.usecases.user_usecases import UserUseCases

logger = get_logger(__name__)


class MessageHandler:
    """Classe responsável por lidar com mensagens não-comando."""

    def __init__(self, user_usecases: UserUseCases):
        self._user_usecases = user_usecases

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
