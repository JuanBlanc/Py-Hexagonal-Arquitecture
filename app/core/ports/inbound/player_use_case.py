import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from core.domain.entities.player import Player


class PlayerUseCase(ABC):
    @abstractmethod
    async def register_player(self, username: str, display_name: str, region: str) -> Player: ...

    @abstractmethod
    async def get_player(self, player_id: uuid.UUID) -> Player: ...

    @abstractmethod
    async def list_players(self, limit: int, offset: int) -> Sequence[Player]: ...

    @abstractmethod
    async def update_player(self, player_id: uuid.UUID, changes: dict[str, Any]) -> Player: ...

    @abstractmethod
    async def delete_player(self, player_id: uuid.UUID) -> None: ...
