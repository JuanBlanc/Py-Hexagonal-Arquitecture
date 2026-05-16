from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from adapters.persistence.postgres.repositories.game_repository import PostgresGameRepository
from adapters.persistence.postgres.repositories.match_repository import PostgresMatchRepository
from adapters.persistence.postgres.repositories.player_repository import PostgresPlayerRepository
from adapters.persistence.postgres.repositories.score_repository import PostgresScoreRepository
from core.ports.outbound.unit_of_work import UnitOfWork


class PostgresUnitOfWork(UnitOfWork):
    """UoW sobre una única AsyncSession compartida por todos los repos del caso de uso.

    Los repos no commitean; el commit/rollback lo decide el context manager del
    puerto (al salir bien / ante excepción), es decir, el caso de uso.
    """

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    async def _begin(self) -> None:
        self._session = self._session_factory()
        self.players = PostgresPlayerRepository(self._session)
        self.games = PostgresGameRepository(self._session)
        self.matches = PostgresMatchRepository(self._session)
        self.scores = PostgresScoreRepository(self._session)

    async def commit(self) -> None:
        if self._session is not None:
            await self._session.commit()

    async def rollback(self) -> None:
        if self._session is not None:
            await self._session.rollback()

    async def _close(self) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None
