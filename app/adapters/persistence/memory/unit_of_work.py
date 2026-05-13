from adapters.persistence.memory.game_repository import InMemoryGameRepository
from adapters.persistence.memory.match_repository import InMemoryMatchRepository
from adapters.persistence.memory.player_repository import InMemoryPlayerRepository
from adapters.persistence.memory.score_repository import InMemoryScoreRepository
from adapters.persistence.memory.store import InMemoryStore
from core.ports.outbound.unit_of_work import UnitOfWork


class MemoryUnitOfWork(UnitOfWork):
    """UoW sobre el store en memoria compartido.

    El store es único y mutable: las escrituras ya quedan visibles, así que
    commit/rollback son no-ops (no hay transacción que confirmar ni deshacer).
    """

    def __init__(self, store: InMemoryStore) -> None:
        self._store = store

    async def _begin(self) -> None:
        self.players = InMemoryPlayerRepository(self._store)
        self.games = InMemoryGameRepository(self._store)
        self.matches = InMemoryMatchRepository(self._store)
        self.scores = InMemoryScoreRepository(self._store)

    async def commit(self) -> None:
        return None

    async def rollback(self) -> None:
        return None

    async def _close(self) -> None:
        return None
