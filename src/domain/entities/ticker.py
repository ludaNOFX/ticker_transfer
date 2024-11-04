from datetime import datetime

from pydantic import BaseModel


class Ticker(BaseModel):
    """Ticker entity"""

    id: int
    ticker: str
    price: float
    timestamp: datetime


