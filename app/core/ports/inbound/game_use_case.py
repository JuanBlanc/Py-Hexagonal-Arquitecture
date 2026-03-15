import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence

from core.domain.entities.game import Game


class GameUseCase(ABC):
    @abstractmethod
    async def add_game(self, title: str, genre: str, max_players: int) -> Game: ...

    @abstractmethod
    async def get_game(self, game_id: uuid.UUID) -> Game: ...

    @abstractmethod
    async def list_games(self, limit: int, offset: int) -> Sequence[Game]: ...

    @abstractmethod
    async def remove_game(self, game_id: uuid.UUID) -> None: ...
