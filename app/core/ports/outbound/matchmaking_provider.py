from abc import ABC, abstractmethod
from collections.abc import Sequence

from core.domain.entities.player import Player


class MatchmakingProvider(ABC):
    @abstractmethod
    async def select_opponents(
        self, player: Player, candidate_pool: Sequence[Player], desired_count: int
    ) -> Sequence[Player]: ...
