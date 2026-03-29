import uuid
from collections.abc import Sequence
from dataclasses import replace
from datetime import datetime, timezone

from adapters.persistence.memory.store import InMemoryStore
from core.domain.entities.game import Game
from core.ports.outbound.game_repository import GameRepository


class InMemoryGameRepository(GameRepository):
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    async def list(self, limit: int, offset: int) -> Sequence[Game]:
        all_games = list(self.store.games.values())
        return all_games[offset : offset + limit]

    async def get(self, game_id: uuid.UUID) -> Game | None:
        return self.store.games.get(game_id)

    async def add(self, game: Game) -> Game:
        persisted_game = replace(
            game, game_id=uuid.uuid4(), created_at=datetime.now(timezone.utc)
        )
        self.store.games[persisted_game.game_id] = persisted_game
        return persisted_game

    async def remove(self, game: Game) -> None:
        self.store.games.pop(game.game_id, None)
