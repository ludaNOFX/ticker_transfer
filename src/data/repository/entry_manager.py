import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto.tickers import TickerDTO
from src.data.models import TickerModel
from src.domain.entities.ticker import Ticker
from src.domain.exception.base import BdError
from src.domain.interfaces.repository.entry_manager import IEntryRepository

logger = logging.getLogger(__name__)


def model_to_dto(model: TickerModel, obj: TickerDTO | None = None) -> Ticker:
    if obj:
        obj = Ticker(id=model.id, ticker=obj.ticker, price=obj.price, timestamp=obj.timestamp)  # type: ignore
    else:
        obj = Ticker(id=model.id, ticker=model.ticker, price=model.price, timestamp=model.timestamp)  # type: ignore
    return obj  # type: ignore


class EntryRepository(IEntryRepository):
    def __init__(self, db_context: AsyncSession) -> None:
        self.__db_context = db_context

    async def check(self, *, obj: TickerDTO) -> Ticker | None:
        stmt = select(TickerModel).where(TickerModel.ticker == obj.ticker)

        try:
            res = await self.__db_context.scalar(stmt)
        except IntegrityError as error:
            logger.exception(f"EntryRepository: {error}")
            raise BdError(msg="") from error
        if not res:
            return None

        return model_to_dto(model=res, obj=obj)
