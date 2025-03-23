from telegram import Update
from telegram.ext import ContextTypes
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class UnknownHandler:
    """Classe responsável por lidar com comandos desconhecidos."""

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Responde a comandos desconhecidos."""
        if update.message:
            await update.message.reply_text(
                "Desculpe, não entendi esse comando. Por favor, use um comando válido."
            )
        else:
            logger.warning("Mensagem de atualização não encontrada.")
