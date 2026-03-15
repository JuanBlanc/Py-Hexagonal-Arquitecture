import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence

from core.domain.entities.match import Match


class MatchRepository(ABC):
    @abstractmethod
    async def list(self, limit: int, offset: int) -> Sequence[Match]: ...

    @abstractmethod
    async def get(self, match_id: uuid.UUID) -> Match | None: ...

    @abstractmethod
    async def add(self, match: Match) -> Match: ...

    @abstractmethod
    async def update(self, match: Match) -> Match: ...
