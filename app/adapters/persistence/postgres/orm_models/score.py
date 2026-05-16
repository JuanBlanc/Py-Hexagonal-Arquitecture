import uuid
from datetime import datetime

from sqlalchemy import DDL, DateTime, Index, Integer, event, text
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from adapters.persistence.postgres.base import Base


class ScoreModel(Base):
    """Hypertable TimescaleDB, particionada por `recorded_at`.

    TimescaleDB exige que la columna de partición forme parte de toda PK/unique,
    de ahí la PK compuesta (score_id, recorded_at).
    """

    __tablename__ = "scores"
    __table_args__ = (
        Index("ix_scores_game_recorded", "game_id", text("recorded_at DESC")),
        Index("ix_scores_match_recorded", "match_id", text("recorded_at DESC")),
    )

    score_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True, server_default=text("now()")
    )
    match_id: Mapped[uuid.UUID] = mapped_column(PgUUID(as_uuid=True), nullable=False)
    game_id: Mapped[uuid.UUID] = mapped_column(PgUUID(as_uuid=True), nullable=False)
    player_id: Mapped[uuid.UUID] = mapped_column(PgUUID(as_uuid=True), nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)


# Convierte `scores` en hypertable justo después de crear la tabla, vía SQLAlchemy.
event.listen(
    ScoreModel.__table__,
    "after_create",
    DDL("SELECT create_hypertable('scores', 'recorded_at', if_not_exists => TRUE)"),
)
