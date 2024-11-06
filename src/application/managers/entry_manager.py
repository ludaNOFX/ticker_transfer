from src.application.dto.tickers import TickerDTO, TickerUpdateDTO, TickerCreateDTO
from src.domain.interfaces.uow import IUnitOfWork


class EntryManager:
    def __init__(self, *, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, *, obj: TickerDTO) -> TickerUpdateDTO | TickerCreateDTO:
        async with self.uow as uow:
            ticker = await self.uow.manager.check(obj=obj)

        if ticker is not None:
            return TickerUpdateDTO(**ticker.model_dump())

        return obj.to_obj()
