import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence

from core.domain.entities.score import Score


class ScoreRepository(ABC):
    @abstractmethod
    async def add(self, score: Score) -> Score: ...

    @abstractmethod
    async def list_for_match(self, match_id: uuid.UUID) -> Sequence[Score]: ...

    @abstractmethod
    async def leaderboard_for_game(self, game_id: uuid.UUID, limit: int) -> Sequence[Score]: ...
