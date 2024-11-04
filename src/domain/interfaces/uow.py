from abc import ABC, abstractmethod

from src.domain.interfaces.repository.entry_manager import IEntryRepository
from src.domain.interfaces.repository.tickers import ITickersRepository


class IUnitOfWork(ABC):

    @property
    @abstractmethod
    def manager(self) -> IEntryRepository:
        ...

    @property
    @abstractmethod
    def ticker(self) -> ITickersRepository:
        ...

    @abstractmethod
    async def __aenter__(self) -> "IUnitOfWork":
        ...

    @abstractmethod
    async def __aexit__(self, *args) -> None:
        ...

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...