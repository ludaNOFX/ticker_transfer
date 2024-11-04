from abc import ABC, abstractmethod

from src.application.dto.tickers import TickerCreateDTO, TickerUpdateDTO


class ITickersRepository(ABC):
    @abstractmethod
    async def create(self, *, obj: TickerCreateDTO) -> None:
        """Create tickers

        Args:
            obj (TickerCreateDTO): DTO for creating ticker object

        Returns:
            None

        Raises:
            RepoError: Repository error
            EntityNotCreated: Ticker not created

        """

    @abstractmethod
    async def update(self, *, obj: TickerUpdateDTO) -> None:
        """Create tickers

        Args:
            obj (TickerUpdateDTO): DTO for creating ticker object

        Returns:
            None

        Raises:
            RepoError: Repository error

        """
