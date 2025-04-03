import logging
from src.data.database_interface import DatabaseInterface

logger = logging.getLogger(__name__)


class DatabaseInitializationService:
    """
    Serviço para inicialização e verificação do banco de dados.

    Esta classe segue o princípio de responsabilidade única do SOLID,
    centralizando a lógica de inicialização e verificação do banco de dados.
    """

    def __init__(self, database: DatabaseInterface):
        """
        Inicializa o serviço com uma interface de banco de dados.

        Args:
            database: Interface do banco de dados a ser verificada e inicializada.
        """
        self.database = database

    def initialize(self) -> None:
        """
        Verifica o estado do banco de dados e inicializa as tabelas faltantes se necessário.
        """
        logger.info("Verificando o estado do banco de dados...")
        db_state = self.database.verify_database()

        if not db_state["all_tables_exist"]:
            logger.warning(f"Tabelas faltantes: {db_state['missing_tables']}")
            logger.info("Criando tabelas faltantes no banco de dados...")
            self.database.create_tables()
            logger.info("Tabelas criadas com sucesso!")
        else:
            logger.info(
                f"Banco de dados verificado. Todas as {len(db_state['existing_tables'])} tabelas estão configuradas corretamente."
            )
