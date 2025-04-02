from src.config.logging_config import configure_logging
from src.containers import Container

# Configura o logging antes de qualquer operação
logger = configure_logging()


def main():
    """Função principal para iniciar o bot."""
    # Inicializar o container de dependências
    container = Container()

    # Inicialização do banco de dados através do serviço especializado
    container.database_initialization_service().initialize()

    # Inicializando o bot
    logger.info("Inicializando o bot Telegram...")
    bot = container.telegram_bot()

    # Inicia o bot (método bloqueante)
    bot.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Erro ao executar o bot: {e}")
        raise
