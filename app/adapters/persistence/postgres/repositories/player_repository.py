import uuid
from collections.abc import Sequence
from datetime import datetime, timezone

from sqlalchemy import select

from adapters.persistence.postgres.orm_models.player import PlayerModel
from adapters.persistence.postgres.repositories.base import BaseRepository
from core.domain.entities.player import Player
from core.domain.errors import EntityNotFound
from core.ports.outbound.player_repository import PlayerRepository


class PostgresPlayerRepository(BaseRepository, PlayerRepository):
    @staticmethod
    def _to_entity(row: PlayerModel) -> Player:
        return Player(
            username=row.username,
            display_name=row.display_name,
            region=row.region,
            level=row.level,
            player_id=row.player_id,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    async def list(self, limit: int, offset: int) -> Sequence[Player]:
        result = await self.session.execute(
            select(PlayerModel).order_by(PlayerModel.created_at).limit(limit).offset(offset)
        )
        return [self._to_entity(row) for row in result.scalars().all()]

    async def get(self, player_id: uuid.UUID) -> Player | None:
        row = await self.session.get(PlayerModel, player_id)
        return self._to_entity(row) if row is not None else None

    async def find_by_username(self, username: str) -> Player | None:
        result = await self.session.execute(
            select(PlayerModel).where(PlayerModel.username == username)
        )
        row = result.scalar_one_or_none()
        return self._to_entity(row) if row is not None else None

    async def add(self, player: Player) -> Player:
        row = PlayerModel(
            player_id=player.player_id or uuid.uuid4(),
            username=player.username,
            display_name=player.display_name,
            region=player.region,
            level=player.level,
        )
        self.session.add(row)
        await self._flush(row)
        return self._to_entity(row)

    async def update(self, player: Player) -> Player:
        row = await self.session.get(PlayerModel, player.player_id)
        if row is None:
            raise EntityNotFound(f"player not found: {player.player_id}")
        row.username = player.username
        row.display_name = player.display_name
        row.region = player.region
        row.level = player.level
        row.updated_at = datetime.now(timezone.utc)
        await self._flush(row)
        return self._to_entity(row)

    async def remove(self, player: Player) -> None:
        row = await self.session.get(PlayerModel, player.player_id)
        if row is None:
            return
        await self._delete(row)
