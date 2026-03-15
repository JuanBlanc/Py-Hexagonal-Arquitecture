import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence

from core.domain.entities.match import Match


class MatchUseCase(ABC):
    @abstractmethod
    async def create_match(self, game_id: uuid.UUID, host_player_id: uuid.UUID) -> Match: ...

    @abstractmethod
    async def get_match(self, match_id: uuid.UUID) -> Match: ...

    @abstractmethod
    async def list_matches(self, limit: int, offset: int) -> Sequence[Match]: ...

    @abstractmethod
    async def start_match(self, match_id: uuid.UUID) -> Match: ...

    @abstractmethod
    async def finish_match(self, match_id: uuid.UUID) -> Match: ...

    @abstractmethod
    async def abort_match(self, match_id: uuid.UUID) -> Match: ...
