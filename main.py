import asyncio
from src.config.logging_config import configure_logging
from src.containers import Container

# Configura o logging antes de qualquer operação
logger = configure_logging()


async def main():
    """Função principal para iniciar o bot."""
    # Inicializar o container de dependências
    container = Container()

    # Criando o banco de dados e as tabelas (se não existirem)
    container.database().create_tables()

    # Inicializando o bot
    logger.info("Inicializando o bot Telegram...")
    bot = container.telegram_bot()

    # Iniciando o bot
    await bot.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Erro ao executar o bot: {e}")
        raise
