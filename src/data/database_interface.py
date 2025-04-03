from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from typing import List, Dict, Any


class DatabaseInterface(ABC):
    """Interface para gerenciamento de conexões e operações com banco de dados."""

    @abstractmethod
    def create_tables(self) -> None:
        """Cria todas as tabelas definidas nos modelos."""
        pass

    @abstractmethod
    def get_session(self) -> Session:
        """
        Retorna uma nova sessão do banco de dados.

        Returns:
            Uma sessão do banco de dados.
        """
        pass

    @abstractmethod
    def get_engine(self) -> Engine:
        """
        Retorna a engine de conexão com o banco de dados.

        Returns:
            A engine de conexão configurada.
        """
        pass

    @abstractmethod
    def verify_database(self) -> Dict[str, Any]:
        """
        Verifica se o banco de dados existe e se todas as tabelas estão configuradas.

        Returns:
            Dicionário com informações sobre o estado do banco de dados.
        """
        pass
