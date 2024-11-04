from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.data.repository.entry_manager import EntryRepository
from src.domain.interfaces.repository.entry_manager import IEntryRepository
from src.domain.interfaces.repository.tickers import ITickersRepository
from src.domain.interfaces.uow import IUnitOfWork
from src.data.repository.tickers import TickersRepository


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.__session_factory = session_factory
        self._ticker: ITickersRepository | None = None
        self._manager: IEntryRepository | None = None
        self.__session: AsyncSession | None = None

    @property
    def ticker(self) -> ITickersRepository:
        if self._ticker:
            return self._ticker
        raise ValueError("UoW not in context")

    @property
    def manager(self) -> IEntryRepository:
        if self._manager:
            return self._manager
        print("ТУт какаято проблема")
        raise ValueError("UoW not in context")

    @property
    def _session(self) -> AsyncSession:
        if self.__session is None:
            raise ValueError("UoW not in context")
        return self.__session

    async def __aenter__(self) -> IUnitOfWork:
        self.__session = self.__session_factory()
        self._ticker = TickersRepository(self._session)
        self._manager = EntryRepository(self._session)
        return  self

    async def __aexit__(self, *args) -> None:
        await self._session.rollback()
        await self._session.close()
        self.__session = None

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()