from dataclasses import dataclass
from datetime import datetime

from src.domain.ctx.ticker.schemas.update_ticker import UpdateFltr


@dataclass
class TickerCreateDTO:
    ticker: str
    price: float
    timestamp: datetime


@dataclass
class TickerDTO:
    ticker: str
    price: float
    timestamp: datetime

    def to_obj(self) -> TickerCreateDTO:
        return TickerCreateDTO(ticker=self.ticker, price=self.price, timestamp=self.timestamp)

@dataclass
class TickerUpdateDTO:
    id: int
    ticker: str
    price: float
    timestamp: datetime

    def to_obj(self) -> UpdateFltr:
        return UpdateFltr(price=self.price, timestamp=self.timestamp)


