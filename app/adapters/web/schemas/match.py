import uuid
from datetime import datetime

from pydantic import BaseModel

from core.domain.entities.match import Match
from core.domain.enums.match_status import MatchStatus


class CreateMatchRequest(BaseModel):
    game_id: uuid.UUID
    host_player_id: uuid.UUID


class MatchResponse(BaseModel):
    match_id: uuid.UUID
    game_id: uuid.UUID
    host_player_id: uuid.UUID
    status: MatchStatus
    player_ids: list[uuid.UUID]
    started_at: datetime | None
    finished_at: datetime | None
    created_at: datetime | None

    @classmethod
    def from_entity(cls, match: Match) -> "MatchResponse":
        return cls(
            match_id=match.match_id,
            game_id=match.game_id,
            host_player_id=match.host_player_id,
            status=match.status,
            player_ids=match.player_ids,
            started_at=match.started_at,
            finished_at=match.finished_at,
            created_at=match.created_at,
        )
