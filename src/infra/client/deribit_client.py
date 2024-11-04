import logging
from datetime import timezone, datetime
import aiohttp
from typing import Dict, Any

from src.application.dto.tickers import TickerUpdateDTO
from src.application.managers.entry_manager import EntryManager
from src.application.usecases.tickers_create import TickersCreateUsecase
from src.application.usecases.tickers_update import TickersUpdateUsecase
from src.domain.interfaces.uow import IUnitOfWork
from src.infra.client.schemas.tickers import TickersListSchema

logger = logging.getLogger(__name__)


class DeribitClient:
    def __init__(self, base_url: str = "https://www.deribit.com/api/v2/public") -> None:
        self.__base_url = base_url

    async def __fetch_price(self, ticker: str) -> Dict[str, Any]:
        """Асинхронно получает текущую цену"""
        async with aiohttp.ClientSession() as session:
            endpoint = f"{self.__base_url}/get_index_price?index_name={ticker}"
            async with session.get(endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "ticker": ticker,
                        "price": data["result"]["index_price"],
                        "timestamp": datetime.now(timezone.utc).replace(tzinfo=None)
                    }
                else:
                    body = await response.text()
                    logger.exception(f"Error fetching data for {ticker}: {response.status} - {body}")
                    raise Exception(f"Error fetching data for {ticker}: {response.status} - {body}")

    async def get_prices(self, tickers: list[str]) -> TickersListSchema:
        results = []
        for ticker in tickers:
            try:
                data = await self.__fetch_price(ticker)
                results.append(data)
            except Exception as e:
                logger.exception(f"Failed to fetch price for {ticker}: {e}")

        results = {'tickers': results}
        return TickersListSchema(**results)


# задача для получения цен
async def fetch_and_save_prices_periodically(
        uow_factory: IUnitOfWork,
        tickers: list,
) -> None:
    client = DeribitClient()
    prices = await client.get_prices(tickers)
    for ticker in prices.tickers:
        new_obj = ticker.to_obj()
        logger.info(f"get obj ---> {new_obj}")
        em = EntryManager(uow=uow_factory)
        obj = await em(obj=new_obj)
        logger.info(f"check obj ---> {obj}")
        if isinstance(obj, TickerUpdateDTO):
            uc = TickersUpdateUsecase(uow=uow_factory)
            await uc(update_obj=obj)
            logger.info(f"update obj ---> {obj}")
        else:
            uc = TickersCreateUsecase(uow=uow_factory)
            await uc(create_obj=obj)
            logger.info(f"create obj ---> {obj}")
