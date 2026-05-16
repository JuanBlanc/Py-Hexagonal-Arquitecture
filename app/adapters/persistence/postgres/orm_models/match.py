import uuid
from datetime import datetime

from sqlalchemy import ARRAY, DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from adapters.persistence.postgres.base import Base


class MatchModel(Base):
    __tablename__ = "matches"

    match_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    game_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("games.game_id"), nullable=False
    )
    host_player_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("players.player_id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String, nullable=False)
    # Array de UUIDs para calcar `Match.player_ids`. Alternativa más normalizada:
    # una tabla puente `match_players(match_id, player_id)`.
    player_ids: Mapped[list[uuid.UUID]] = mapped_column(
        ARRAY(PgUUID(as_uuid=True)), nullable=False, server_default=text("'{}'")
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
