import uuid
from dataclasses import dataclass, field
from datetime import datetime

from core.domain.enums.match_status import MatchStatus


@dataclass
class Match:
    game_id: uuid.UUID
    host_player_id: uuid.UUID
    status: MatchStatus
    player_ids: list[uuid.UUID] = field(default_factory=list)
    match_id: uuid.UUID | None = field(default=None)
    started_at: datetime | None = field(default=None)
    finished_at: datetime | None = field(default=None)
    created_at: datetime | None = field(default=None)
