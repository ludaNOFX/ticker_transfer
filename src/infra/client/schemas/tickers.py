from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.application.dto.tickers import TickerDTO


class UsdCreateSchema(BaseModel):
    ticker: str
    price: float
    timestamp: datetime

    def to_obj(self) -> TickerDTO:
        return TickerDTO(ticker=self.ticker, price=self.price, timestamp=self.timestamp)


class TickersListSchema(BaseModel):
    tickers: List[UsdCreateSchema]







