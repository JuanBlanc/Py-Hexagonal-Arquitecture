import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence

from core.domain.entities.game import Game


class GameRepository(ABC):
    @abstractmethod
    async def list(self, limit: int, offset: int) -> Sequence[Game]: ...

    @abstractmethod
    async def get(self, game_id: uuid.UUID) -> Game | None: ...

    @abstractmethod
    async def add(self, game: Game) -> Game: ...

    @abstractmethod
    async def remove(self, game: Game) -> None: ...
