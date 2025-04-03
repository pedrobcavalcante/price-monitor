from typing import Optional, Dict, Any, Tuple
from telegram import Update
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.config.logging_config import get_logger

logger = get_logger(__name__)


class UserUseCases:
    """Casos de uso relacionados a usuários."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def verify_or_create_user(self, telegram_data: Dict[str, Any]) -> Optional[User]:
        """
        Verifica se um usuário existe e o cria se necessário.

        Args:
            telegram_data: Dados do usuário obtidos do Telegram

        Returns:
            Objeto de usuário ou None em caso de erro
        """
        try:
            telegram_id = telegram_data.get("id")
            if not telegram_id:
                logger.error("ID do Telegram não fornecido nos dados")
                return None

            user = self._user_repository.find_by_telegram_id(telegram_id)

            if not user:
                # Cria um novo usuário com dados do Telegram
                user_data = {
                    "telegram_id": telegram_id,
                    "username": telegram_data.get("username"),
                    "first_name": telegram_data.get("first_name", "Usuário"),
                    "last_name": telegram_data.get("last_name"),
                }

                user = self._user_repository.create(user_data)
                logger.info(f"Novo usuário registrado: {user}")

            return user

        except Exception as e:
            logger.error(f"Erro ao verificar/criar usuário: {e}")
            return None

    async def verify_telegram_user(self, update: Update) -> Tuple[bool, Optional[User]]:
        """
        Verifica se o usuário do Telegram está registrado.

        Args:
            update: O objeto Update do Telegram.

        Returns:
            Tupla contendo:
                - Boolean indicando se o usuário é válido
                - Objeto User se encontrado, None caso contrário
        """
        if not update.effective_user:
            logger.warning("Usuário não encontrado na atualização.")
            return False, None

        user_data = update.effective_user.to_dict()
        user = self.verify_or_create_user(user_data)

        return user is not None, user

    async def register_user(self, update: Update) -> Tuple[bool, str]:
        """
        Registra um novo usuário a partir da atualização do Telegram.

        Args:
            update: O objeto Update do Telegram.

        Returns:
            Tupla contendo:
                - Boolean indicando se o registro foi bem-sucedido
                - Mensagem informativa sobre o resultado
        """
        if not update.effective_user:
            return False, "Não foi possível identificar o usuário."

        user_data = update.effective_user.to_dict()

        try:
            telegram_id = user_data.get("id")
            if not telegram_id:
                return False, "ID do Telegram não encontrado."

            # Verifica se o usuário já existe
            existing_user = self._user_repository.find_by_telegram_id(telegram_id)
            if existing_user:
                return True, "Usuário já registrado."

            # Cria um novo usuário
            user_data = {
                "telegram_id": telegram_id,
                "username": user_data.get("username"),
                "first_name": user_data.get("first_name", "Usuário"),
                "last_name": user_data.get("last_name"),
                "is_admin": False,  # Por padrão, novos usuários não são administradores
            }

            self._user_repository.create(user_data)
            return True, "Registro realizado com sucesso!"

        except Exception as e:
            logger.error(f"Erro ao registrar usuário: {e}")
            return (
                False,
                "Ocorreu um erro ao processar o registro. Tente novamente mais tarde.",
            )
