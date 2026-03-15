import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence

from core.domain.entities.player import Player


class MatchmakingUseCase(ABC):
    @abstractmethod
    async def find_opponents(
        self, player_id: uuid.UUID, desired_count: int
    ) -> Sequence[Player]: ...
