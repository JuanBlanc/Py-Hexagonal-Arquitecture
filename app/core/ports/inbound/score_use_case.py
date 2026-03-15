import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence

from core.domain.entities.score import Score


class ScoreUseCase(ABC):
    @abstractmethod
    async def submit_score(
        self, match_id: uuid.UUID, player_id: uuid.UUID, points: int
    ) -> Score: ...

    @abstractmethod
    async def list_match_scores(self, match_id: uuid.UUID) -> Sequence[Score]: ...

    @abstractmethod
    async def leaderboard(self, game_id: uuid.UUID, limit: int) -> Sequence[Score]: ...
