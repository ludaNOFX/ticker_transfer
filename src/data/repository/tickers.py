import logging
from dataclasses import asdict
from typing import cast

from asyncpg import UniqueViolationError
from sqlalchemy import insert, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto.tickers import TickerCreateDTO, TickerUpdateDTO
from src.data.models.ticker.ticker import TickerModel
from src.domain.exception.base import EntityNotCreated, EntityNotFound, BdError
from src.domain.interfaces.repository.tickers import ITickersRepository
from src.utils import as_dict_skip_none

logger = logging.getLogger(__name__)


class TickersRepository(ITickersRepository):
    def __init__(self, db_context: AsyncSession) -> None:
        self.__db_context = db_context

    async def create(self, *, obj: TickerCreateDTO) -> None:
        stmt = insert(TickerModel).values(**asdict(obj)).returning(TickerModel)
        try:
            res = await self.__db_context.scalar(stmt)
        except IntegrityError as error:
            error.orig = cast(BaseException, error.orig)
            logger.exception(f"TickersRepository method <create>: {error}")
            if isinstance(error.orig.__cause__, UniqueViolationError):
                raise EntityNotCreated(msg="Uniq failed") from error
            raise EntityNotCreated(msg="") from error
        if not res:
            raise EntityNotFound(msg="")

    async def update(self, *, obj: TickerUpdateDTO) -> None:
        fltr_obj = obj.to_obj()
        stmt = update(
            TickerModel).where(
            TickerModel.id == obj.id).values(**as_dict_skip_none(fltr_obj)).returning(TickerModel)
        try:
            res = await self.__db_context.scalar(stmt)
        except IntegrityError as error:
            logger.exception(f"TickersRepository method <update>: {error}")
            raise BdError(msg="") from error
        if not res:
            raise EntityNotFound(msg="")
