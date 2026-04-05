import uuid
from datetime import datetime

from pydantic import BaseModel

from core.domain.entities.player import Player


class RegisterPlayerRequest(BaseModel):
    username: str
    display_name: str
    region: str


class UpdatePlayerRequest(BaseModel):
    display_name: str | None = None
    region: str | None = None
    level: int | None = None


class PlayerResponse(BaseModel):
    player_id: uuid.UUID
    username: str
    display_name: str
    region: str
    level: int
    created_at: datetime | None
    updated_at: datetime | None

    @classmethod
    def from_entity(cls, player: Player) -> "PlayerResponse":
        return cls(
            player_id=player.player_id,
            username=player.username,
            display_name=player.display_name,
            region=player.region,
            level=player.level,
            created_at=player.created_at,
            updated_at=player.updated_at,
        )
