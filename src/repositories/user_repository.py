from typing import Optional, Dict, Any

from src.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.data.datasources.user_datasource import UserDatasource
from src.models.user import User


class UserRepository(UserRepositoryInterface):
    """Repositório para operações relacionadas a usuários."""

    def __init__(self, user_datasource: UserDatasource):
        """
        Inicializa o repositório com um datasource.

        Args:
            user_datasource: Implementação de UserDatasource
        """
        self._datasource = user_datasource

    def find_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """
        Busca um usuário pelo ID do Telegram.

        Args:
            telegram_id: ID do usuário no Telegram

        Returns:
            Usuário encontrado ou None se não existir
        """
        return self._datasource.find_by_telegram_id(telegram_id)

    def create(self, user_data: Dict[str, Any]) -> User:
        """
        Cria um novo usuário.

        Args:
            user_data: Dicionário com os dados do usuário

        Returns:
            Usuário criado
        """
        return self._datasource.create(user_data)

    def update(self, user: User) -> User:
        """
        Atualiza um usuário existente.

        Args:
            user: Objeto de usuário com alterações

        Returns:
            Usuário atualizado
        """
        return self._datasource.update(user)
