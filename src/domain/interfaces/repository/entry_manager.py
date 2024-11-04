from abc import ABC, abstractmethod

from src.application.dto.tickers import TickerDTO
from src.domain.entities.ticker import Ticker


class IEntryRepository(ABC):
    @abstractmethod
    async def check(self, *, obj: TickerDTO) -> Ticker | None:
        """Check tickers in db

        Args:
            obj (TickerDTO): DTO for checking ticker object in db

        Returns:
            None

        Raises:
            RepoError: Repository error

        """