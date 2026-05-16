"""Modelos ORM SQLAlchemy: mapean las entidades de dominio a tablas Postgres.

Solo `scores` se convierte en hypertable de TimescaleDB (evento DDL en score.py).
El resto son tablas relacionales normales.

Estos modelos son detalle del adaptador y NO deben filtrarse al núcleo: los
repositorios traducen entre estos modelos y las entidades de `core.domain`.

Importar este paquete registra todos los modelos en `Base.metadata` (lo que
necesita tanto `create_all` como el autogenerate de Alembic). El `Base`
declarativo vive en `adapters.persistence.postgres.base`.
"""

from adapters.persistence.postgres.orm_models.game import GameModel
from adapters.persistence.postgres.orm_models.match import MatchModel
from adapters.persistence.postgres.orm_models.player import PlayerModel
from adapters.persistence.postgres.orm_models.score import ScoreModel

__all__ = ["GameModel", "MatchModel", "PlayerModel", "ScoreModel"]
