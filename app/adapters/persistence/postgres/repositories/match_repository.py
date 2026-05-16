import uuid
from collections.abc import Sequence

from sqlalchemy import select

from adapters.persistence.postgres.orm_models.match import MatchModel
from adapters.persistence.postgres.repositories.base import BaseRepository
from core.domain.entities.match import Match
from core.domain.enums.match_status import MatchStatus
from core.domain.errors import EntityNotFound
from core.ports.outbound.match_repository import MatchRepository


class PostgresMatchRepository(BaseRepository, MatchRepository):
    @staticmethod
    def _to_entity(row: MatchModel) -> Match:
        return Match(
            game_id=row.game_id,
            host_player_id=row.host_player_id,
            status=MatchStatus(row.status),
            player_ids=list(row.player_ids),
            match_id=row.match_id,
            started_at=row.started_at,
            finished_at=row.finished_at,
            created_at=row.created_at,
        )

    async def list(self, limit: int, offset: int) -> Sequence[Match]:
        result = await self.session.execute(
            select(MatchModel).order_by(MatchModel.created_at).limit(limit).offset(offset)
        )
        return [self._to_entity(row) for row in result.scalars().all()]

    async def get(self, match_id: uuid.UUID) -> Match | None:
        row = await self.session.get(MatchModel, match_id)
        return self._to_entity(row) if row is not None else None

    async def add(self, match: Match) -> Match:
        row = MatchModel(
            match_id=match.match_id or uuid.uuid4(),
            game_id=match.game_id,
            host_player_id=match.host_player_id,
            status=match.status.value,
            player_ids=list(match.player_ids),
            started_at=match.started_at,
            finished_at=match.finished_at,
        )
        self.session.add(row)
        await self._flush(row)
        return self._to_entity(row)

    async def update(self, match: Match) -> Match:
        row = await self.session.get(MatchModel, match.match_id)
        if row is None:
            raise EntityNotFound(f"match not found: {match.match_id}")
        row.status = match.status.value
        row.player_ids = list(match.player_ids)
        row.started_at = match.started_at
        row.finished_at = match.finished_at
        await self._flush(row)
        return self._to_entity(row)
