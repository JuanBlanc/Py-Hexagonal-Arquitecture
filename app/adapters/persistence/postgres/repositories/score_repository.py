import uuid
from collections.abc import Sequence

from sqlalchemy import select

from adapters.persistence.postgres.orm_models.score import ScoreModel
from adapters.persistence.postgres.repositories.base import BaseRepository
from core.domain.entities.score import Score
from core.ports.outbound.score_repository import ScoreRepository


class PostgresScoreRepository(BaseRepository, ScoreRepository):
    """Adaptador sobre la hypertable `scores` de TimescaleDB."""

    @staticmethod
    def _to_entity(row: ScoreModel) -> Score:
        return Score(
            match_id=row.match_id,
            game_id=row.game_id,
            player_id=row.player_id,
            points=row.points,
            score_id=row.score_id,
            recorded_at=row.recorded_at,
        )

    async def add(self, score: Score) -> Score:
        row = ScoreModel(
            score_id=score.score_id or uuid.uuid4(),
            match_id=score.match_id,
            game_id=score.game_id,
            player_id=score.player_id,
            points=score.points,
        )
        self.session.add(row)
        await self._flush(row)
        return self._to_entity(row)

    async def list_for_match(self, match_id: uuid.UUID) -> Sequence[Score]:
        result = await self.session.execute(
            select(ScoreModel).where(ScoreModel.match_id == match_id).order_by(ScoreModel.recorded_at)
        )
        return [self._to_entity(row) for row in result.scalars().all()]

    async def leaderboard_for_game(self, game_id: uuid.UUID, limit: int) -> Sequence[Score]:
        result = await self.session.execute(
            select(ScoreModel)
            .where(ScoreModel.game_id == game_id)
            .order_by(ScoreModel.points.desc())
            .limit(limit)
        )
        return [self._to_entity(row) for row in result.scalars().all()]
