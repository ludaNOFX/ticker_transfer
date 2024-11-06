from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.db.base_class import Base

@dataclass
class TickerModel(Base):
    __tablename__ = "ticker"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(unique=True)
    price: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[datetime] = mapped_column(DateTime)