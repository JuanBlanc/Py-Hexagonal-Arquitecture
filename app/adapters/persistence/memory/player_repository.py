import uuid
from collections.abc import Sequence
from dataclasses import replace
from datetime import datetime, timezone

from adapters.persistence.memory.store import InMemoryStore
from core.domain.entities.player import Player
from core.domain.errors import EntityNotFound
from core.ports.outbound.player_repository import PlayerRepository


class InMemoryPlayerRepository(PlayerRepository):
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    async def list(self, limit: int, offset: int) -> Sequence[Player]:
        all_players = list(self.store.players.values())
        return all_players[offset : offset + limit]

    async def get(self, player_id: uuid.UUID) -> Player | None:
        return self.store.players.get(player_id)

    async def find_by_username(self, username: str) -> Player | None:
        for player in self.store.players.values():
            if player.username == username:
                return player
        return None

    async def add(self, player: Player) -> Player:
        now = datetime.now(timezone.utc)
        persisted_player = replace(
            player, player_id=uuid.uuid4(), created_at=now, updated_at=now
        )
        self.store.players[persisted_player.player_id] = persisted_player
        return persisted_player

    async def update(self, player: Player) -> Player:
        if player.player_id not in self.store.players:
            raise EntityNotFound(f"player not found: {player.player_id}")
        persisted_player = replace(player, updated_at=datetime.now(timezone.utc))
        self.store.players[persisted_player.player_id] = persisted_player
        return persisted_player

    async def remove(self, player: Player) -> None:
        self.store.players.pop(player.player_id, None)
