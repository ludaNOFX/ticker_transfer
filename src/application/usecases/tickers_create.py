from src.application.dto.tickers import TickerCreateDTO
from src.domain.interfaces.uow import IUnitOfWork


class TickersCreateUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, create_obj: TickerCreateDTO) -> None:
        async with self.uow as uow:
            await self.uow.ticker.create(obj=create_obj)
            await uow.commit()