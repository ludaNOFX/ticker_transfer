from src.application.dto.tickers import TickerUpdateDTO
from src.domain.interfaces.uow import IUnitOfWork


class TickersUpdateUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, update_obj: TickerUpdateDTO) -> None:
        async with self.uow as uow:
            await self.uow.ticker.update(obj=update_obj)
            await uow.commit()
