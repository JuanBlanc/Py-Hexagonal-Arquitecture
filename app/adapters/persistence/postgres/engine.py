from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class Database:
    """Dueño del engine y la fábrica de sesiones async.

    Su ciclo de vida lo gestiona el composition root: se crea al arrancar la app
    y se cierra (`dispose`) al apagarla, enganchado al lifespan ASGI de Falcon.
    La URL se la inyecta el composition root; no se lee del entorno aquí.
    """

    def __init__(self, url: str) -> None:
        self._engine: AsyncEngine = create_async_engine(
            url,
            echo=False,
            pool_pre_ping=True,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
        )

    async def create_schema(self) -> None:
        """Crea el esquema desde los modelos ORM (SQLAlchemy puro).

        Importar el paquete `orm_models` registra todos los modelos en
        `Base.metadata` y engancha los eventos DDL: `CREATE EXTENSION timescaledb`
        antes de las tablas y `create_hypertable('scores', ...)` después.
        """
        from adapters.persistence.postgres import orm_models  # noqa: F401  registra modelos
        from adapters.persistence.postgres.base import Base

        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def dispose(self) -> None:
        await self._engine.dispose()
