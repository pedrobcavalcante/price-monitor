from dependency_injector import containers, providers
from src.config.settings import TELEGRAM_BOT_TOKEN
from src.data.database import Database
from src.data.datasources.sqlite_user_datasource import SQLiteUserDatasource
from src.repositories.user_repository import UserRepository
from src.usecases.user_usecases import UserUseCases
from src.infrastructure.telegram.application_provider import ApplicationProvider
from src.bot.telegram_bot import TelegramBot
from src.bot.handlers.start_handler import StartHandler
from src.bot.handlers.unknown_handler import UnknownHandler
from src.bot.handlers.message_handler import MessageHandler


class Container(containers.DeclarativeContainer):
    """Container para gerenciar as dependências do projeto."""

    # Configurações
    config = providers.Configuration()
    config.telegram_bot_token.from_value(TELEGRAM_BOT_TOKEN)

    # Banco de dados
    database = providers.Singleton(Database)

    # Datasources
    user_datasource = providers.Factory(
        SQLiteUserDatasource,
        database=database,
    )

    # Repositórios
    user_repository = providers.Factory(
        UserRepository,
        user_datasource=user_datasource,
    )

    # Casos de uso
    user_usecases = providers.Factory(
        UserUseCases,
        user_repository=user_repository,
    )

    # Provedor de aplicação do Telegram
    application_provider = providers.Singleton(
        ApplicationProvider,
        token=config.telegram_bot_token,
    )

    # Handlers
    start_handler = providers.Factory(
        StartHandler,
        user_usecases=user_usecases,
    )

    unknown_handler = providers.Factory(
        UnknownHandler,
    )

    message_handler = providers.Factory(
        MessageHandler,
        user_usecases=user_usecases,
    )

    # Bot do Telegram
    telegram_bot = providers.Factory(
        TelegramBot,
        app_provider=application_provider,
        user_usecases=user_usecases,
        start_handler=start_handler,
        unknown_handler=unknown_handler,
        message_handler=message_handler,
    )
