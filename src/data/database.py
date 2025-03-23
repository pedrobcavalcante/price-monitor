from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.models.user import Base

class Database:
    """Classe para gerenciar conexões e operações com o banco de dados."""
    
    def __init__(self, db_path: str = "sqlite:///price_monitor.db"):
        """
        Inicializa a conexão com o banco de dados.
        
        Args:
            db_path: Caminho para o banco de dados SQLite.
        """
        self.engine = create_engine(db_path, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Cria todas as tabelas definidas nos modelos."""
        Base.metadata.create_all(self.engine)
        
    def get_session(self) -> Session:
        """
        Retorna uma nova sessão do banco de dados.
        
        Returns:
            Uma sessão SQLAlchemy.
        """
        return self.SessionLocal()
