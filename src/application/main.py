import asyncio
import logging
import os
from contextlib import asynccontextmanager
import logging_config
from src.application.settings.settings import settings
from src.domain.interfaces.uow import IUnitOfWork
from src.infra.client.deribit_client import fetch_and_save_prices_periodically
from src.infra.db.manager import db_manager
from src.infra.db.uow import SqlAlchemyUnitOfWork

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def get_uow() -> IUnitOfWork:
    return SqlAlchemyUnitOfWork(db_manager.session_factory)


@asynccontextmanager
async def app_lifespan():
    await db_manager.initialize(settings.DATABASE_URL)
    yield
    await db_manager.dispose()


async def main():
    try:
        currencies = str(os.getenv("CURRENCIES"))
        tickers = currencies.split(',')
        logger.info("Init application")
        while True:
            async with app_lifespan():
                uow_factory = get_uow()
                task = asyncio.create_task(
                    fetch_and_save_prices_periodically(uow_factory, tickers))
                try:
                    await task
                except asyncio.CancelledError as e:
                    logger.info(f'Задача fetch_and_save_prices_periodically была отменена {e}')
                    task.cancel()
            await asyncio.sleep(60)
    except KeyboardInterrupt as e:
        logger.info(f'Приложение остановлено пользователем {e}')


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Закончили сбор данных")


