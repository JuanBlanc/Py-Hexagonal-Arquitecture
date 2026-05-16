import uuid
from collections.abc import Sequence

from sqlalchemy import select

from adapters.persistence.postgres.orm_models.game import GameModel
from adapters.persistence.postgres.repositories.base import BaseRepository
from core.domain.entities.game import Game
from core.ports.outbound.game_repository import GameRepository


class PostgresGameRepository(BaseRepository, GameRepository):
    @staticmethod
    def _to_entity(row: GameModel) -> Game:
        return Game(
            title=row.title,
            genre=row.genre,
            max_players=row.max_players,
            game_id=row.game_id,
            created_at=row.created_at,
        )

    async def list(self, limit: int, offset: int) -> Sequence[Game]:
        result = await self.session.execute(
            select(GameModel).order_by(GameModel.created_at).limit(limit).offset(offset)
        )
        return [self._to_entity(row) for row in result.scalars().all()]

    async def get(self, game_id: uuid.UUID) -> Game | None:
        row = await self.session.get(GameModel, game_id)
        return self._to_entity(row) if row is not None else None

    async def add(self, game: Game) -> Game:
        row = GameModel(
            game_id=game.game_id or uuid.uuid4(),
            title=game.title,
            genre=game.genre,
            max_players=game.max_players,
        )
        self.session.add(row)
        await self._flush(row)
        return self._to_entity(row)

    async def remove(self, game: Game) -> None:
        row = await self.session.get(GameModel, game.game_id)
        if row is None:
            return
        await self._delete(row)
