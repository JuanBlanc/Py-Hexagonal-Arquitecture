import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Configuración de la app, leída del entorno en un único punto.

    El composition root la inyecta a los adaptadores: ningún adaptador vuelve a
    leer el entorno por su cuenta, así quedan como piezas pasivas y testeables.
    """

    persistence: str = "memory"
    database_url: str = "postgresql+asyncpg://game:game@db:5432/game_engine"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            persistence=os.environ.get("PERSISTENCE", cls.persistence).lower(),
            database_url=os.environ.get("DATABASE_URL", cls.database_url),
        )


settings = Settings.from_env()
