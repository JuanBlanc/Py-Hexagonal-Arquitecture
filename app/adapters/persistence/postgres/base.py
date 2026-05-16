from sqlalchemy import DDL, event
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# La extensión TimescaleDB se habilita vía SQLAlchemy, antes de crear cualquier
# tabla en `metadata.create_all`. No se usa ningún .sql externo ni init de Docker.
event.listen(
    Base.metadata,
    "before_create",
    DDL("CREATE EXTENSION IF NOT EXISTS timescaledb"),
)
