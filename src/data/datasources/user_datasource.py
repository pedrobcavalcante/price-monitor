from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from src.models.user import User


class UserDatasource(ABC):
    """Interface para fontes de dados de usuários."""

    @abstractmethod
    def find_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """
        Busca um usuário pelo ID do Telegram.

        Args:
            telegram_id: ID do usuário no Telegram

        Returns:
            Usuário encontrado ou None se não existir
        """
        pass

    @abstractmethod
    def create(self, user_data: Dict[str, Any]) -> User:
        """
        Cria um novo usuário.

        Args:
            user_data: Dicionário com os dados do usuário

        Returns:
            Usuário criado
        """
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """
        Atualiza um usuário existente.

        Args:
            user: Objeto de usuário com alterações

        Returns:
            Usuário atualizado
        """
        pass
