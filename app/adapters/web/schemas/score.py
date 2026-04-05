import uuid
from datetime import datetime

from pydantic import BaseModel

from core.domain.entities.score import Score


class SubmitScoreRequest(BaseModel):
    player_id: uuid.UUID
    points: int


class ScoreResponse(BaseModel):
    score_id: uuid.UUID
    match_id: uuid.UUID
    game_id: uuid.UUID
    player_id: uuid.UUID
    points: int
    recorded_at: datetime | None

    @classmethod
    def from_entity(cls, score: Score) -> "ScoreResponse":
        return cls(
            score_id=score.score_id,
            match_id=score.match_id,
            game_id=score.game_id,
            player_id=score.player_id,
            points=score.points,
            recorded_at=score.recorded_at,
        )
