# Migraciones (Alembic)

**Fuente de la verdad: los modelos ORM** en `app/adapters/persistence/postgres/orm_models/`.
Las migraciones NO se escriben a mano: se autogeneran a partir de los modelos.

## Inicializar el esquema

En desarrollo, el esquema se crea directamente desde los modelos vía
`Database.create_schema()` (SQLAlchemy puro: `Base.metadata.create_all`), que
además dispara los eventos DDL de la extensión TimescaleDB y del `create_hypertable`.

## Generar una migración

```bash
DATABASE_URL=postgresql+asyncpg://game:game@localhost:5432/game_engine \
  alembic revision --autogenerate -m "describe el cambio"
```

Alembic compara los modelos (`Base.metadata`) contra la base de datos y escribe el diff.

## Aplicar / revertir

```bash
alembic upgrade head
alembic downgrade -1
```

## Aviso TimescaleDB

`--autogenerate` detecta tablas, columnas e índices, pero **no** captura
`CREATE EXTENSION` ni `create_hypertable` (son DDL fuera del metadata de SQLAlchemy).
Si una migración crea una nueva tabla time-series, hay que añadir a mano su
`op.execute("SELECT create_hypertable(...)")`.
