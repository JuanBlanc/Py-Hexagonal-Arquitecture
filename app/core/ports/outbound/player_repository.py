import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence

from core.domain.entities.player import Player


class PlayerRepository(ABC):
    @abstractmethod
    async def list(self, limit: int, offset: int) -> Sequence[Player]: ...

    @abstractmethod
    async def get(self, player_id: uuid.UUID) -> Player | None: ...

    @abstractmethod
    async def find_by_username(self, username: str) -> Player | None: ...

    @abstractmethod
    async def add(self, player: Player) -> Player: ...

    @abstractmethod
    async def update(self, player: Player) -> Player: ...

    @abstractmethod
    async def remove(self, player: Player) -> None: ...
