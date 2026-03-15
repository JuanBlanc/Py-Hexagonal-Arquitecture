import uuid
from abc import ABC, abstractmethod

from core.domain.entities.score import Score
from core.domain.leaderboard_subscription import LeaderboardSubscription


class LeaderboardPublisher(ABC):
    @abstractmethod
    async def publish(self, score: Score) -> None: ...

    @abstractmethod
    def open_subscription(self, game_id: uuid.UUID) -> LeaderboardSubscription: ...
