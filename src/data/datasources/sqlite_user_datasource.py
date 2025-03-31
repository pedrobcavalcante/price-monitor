from typing import Optional, Dict, Any

from src.data.database import Database
from src.data.datasources.user_datasource import UserDatasource
from src.models.user import User


class SQLiteUserDatasource(UserDatasource):
    """Implementação de UserDatasource para SQLite."""

    def __init__(self, database: Database):
        """
        Inicializa o datasource com uma instância de Database.

        Args:
            database: Instância da classe Database
        """
        self.database = database
        self.ensure_tables_exist()

    def ensure_tables_exist(self) -> None:
        """Garante que as tabelas necessárias existam no banco de dados."""
        engine = self.database.get_engine()
        User.metadata.create_all(engine)

    def find_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """
        Busca um usuário pelo ID do Telegram.

        Args:
            telegram_id: ID do usuário no Telegram

        Returns:
            Usuário encontrado ou None se não existir
        """
        session = self.database.get_session()
        try:
            return session.query(User).filter(User.telegram_id == telegram_id).first()
        finally:
            session.close()

    def create(self, user_data: Dict[str, Any]) -> User:
        """
        Cria um novo usuário.

        Args:
            user_data: Dicionário com os dados do usuário

        Returns:
            Usuário criado
        """
        session = self.database.get_session()
        try:
            user = User(**user_data)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update(self, user: User) -> User:
        """
        Atualiza um usuário existente.

        Args:
            user: Objeto de usuário com alterações

        Returns:
            Usuário atualizado
        """
        session = self.database.get_session()
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
