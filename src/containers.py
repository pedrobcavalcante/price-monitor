from dependency_injector import containers, providers
from src.config.settings import TELEGRAM_BOT_TOKEN
from src.data.database_interface import DatabaseInterface
from src.data.sqlite_database import SQLiteDatabase
from src.data.datasources.sqlite_user_datasource import SQLiteUserDatasource
from src.repositories.user_repository import UserRepository
from src.usecases.user_usecases import UserUseCases
from src.infrastructure.telegram.application_provider import ApplicationProvider
from src.bot.telegram_bot import TelegramBot
from src.bot.handlers.start_handler import StartHandler
from src.bot.handlers.unknown_handler import UnknownHandler
from src.bot.handlers.message_handler import MessageHandler
from src.application.database_initialization_service import (
    DatabaseInitializationService,
)


class Container(containers.DeclarativeContainer):
    """Container para gerenciar as dependências do projeto."""

    # Configurações
    config: providers.Configuration = providers.Configuration()
    config.telegram_bot_token.from_value(TELEGRAM_BOT_TOKEN)

    # Banco de dados - agora tipado com a interface, mas usando a implementação SQLite
    database: providers.Singleton[DatabaseInterface] = providers.Singleton(
        SQLiteDatabase
    )

    # Serviço de inicialização do banco de dados
    database_initialization_service: providers.Factory[
        DatabaseInitializationService
    ] = providers.Factory(
        DatabaseInitializationService,
        database=database,
    )

    # Datasources
    user_datasource: providers.Factory[SQLiteUserDatasource] = providers.Factory(
        SQLiteUserDatasource,
        database=database,
    )

    # Repositórios
    user_repository: providers.Factory[UserRepository] = providers.Factory(
        UserRepository,
        user_datasource=user_datasource,
    )

    # Casos de uso
    user_usecases: providers.Factory[UserUseCases] = providers.Factory(
        UserUseCases,
        user_repository=user_repository,
    )

    # Provedor de aplicação do Telegram
    application_provider: providers.Singleton[ApplicationProvider] = (
        providers.Singleton(
            ApplicationProvider,
            token=config.telegram_bot_token,
        )
    )

    # Handlers
    start_handler: providers.Factory[StartHandler] = providers.Factory(
        StartHandler,
        user_usecases=user_usecases,
    )

    unknown_handler: providers.Factory[UnknownHandler] = providers.Factory(
        UnknownHandler,
    )

    message_handler: providers.Factory[MessageHandler] = providers.Factory(
        MessageHandler,
        user_usecases=user_usecases,
    )

    # Bot do Telegram
    telegram_bot: providers.Factory[TelegramBot] = providers.Factory(
        TelegramBot,
        app_provider=application_provider,
        user_usecases=user_usecases,
        start_handler=start_handler,
        unknown_handler=unknown_handler,
        message_handler=message_handler,
    )
