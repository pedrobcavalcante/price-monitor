from telegram import Update
from telegram.ext import CommandHandler
from datetime import datetime
from loguru import logger

from src.domain.entities import User


class StartCommandUseCase:
    def execute(self, user_id: int, user_name: str) -> str:
        logger.info(f"Usuário {user_id} iniciou o bot")

        user = User(id=user_id, name=user_name, first_access=datetime.now())

        return f"Olá, {user.name}! Bem-vindo ao bot de monitoramento de preços."

    async def start(self, update: Update, context) -> None:
        """Envia uma mensagem quando o comando /start é recebido."""
        if update.message:
            await update.message.reply_text(
                "Olá! Eu sou um bot. Como posso ajudar você?"
            )

    def register_handlers(self, dispatcher) -> None:
        """Registra os manipuladores de comandos no dispatcher."""
        dispatcher.add_handler(CommandHandler("start", self.start))
