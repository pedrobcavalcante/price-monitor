from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from typing import Dict, Any

from src.data.database_interface import DatabaseInterface
from src.models.user import Base


class SQLiteDatabase(DatabaseInterface):
    """Implementação SQLite para gerenciar conexões e operações com o banco de dados."""

    def __init__(self, db_path: str = "sqlite:///price_monitor.db"):
        """
        Inicializa a conexão com o banco de dados SQLite.

        Args:
            db_path: Caminho para o banco de dados SQLite.
        """
        self.engine = create_engine(db_path, echo=False)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def create_tables(self) -> None:
        """Cria todas as tabelas definidas nos modelos."""
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        """
        Retorna uma nova sessão do banco de dados.

        Returns:
            Uma sessão SQLAlchemy.
        """
        return self.SessionLocal()

    def get_engine(self) -> Engine:
        """
        Retorna a engine SQLAlchemy.

        Returns:
            A engine SQLAlchemy configurada.
        """
        return self.engine

    def verify_database(self) -> Dict[str, Any]:
        """
        Verifica se o banco de dados existe e se todas as tabelas estão configuradas.

        Returns:
            Dicionário com informações sobre o estado do banco de dados.
        """
        inspector = inspect(self.engine)
        existing_tables = inspector.get_table_names()
        expected_tables = [table.__tablename__ for table in Base.__subclasses__()]

        missing_tables = [
            table for table in expected_tables if table not in existing_tables
        ]

        return {
            "database_exists": True,  # Se chegou até aqui, o banco existe ou foi criado
            "existing_tables": existing_tables,
            "expected_tables": expected_tables,
            "missing_tables": missing_tables,
            "all_tables_exist": len(missing_tables) == 0,
        }
