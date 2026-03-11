import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Score:
    match_id: uuid.UUID
    game_id: uuid.UUID
    player_id: uuid.UUID
    points: int
    score_id: uuid.UUID | None = field(default=None)
    recorded_at: datetime | None = field(default=None)
