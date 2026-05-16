from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.errors import DuplicateEntity, EntityInUse, ReferenceNotFound

# Códigos de error de PostgreSQL
_UNIQUE_VIOLATION = "23505"
_FK_VIOLATION = "23503"


def _pgcode(exc: IntegrityError) -> str | None:
    # SQLAlchemy envuelve los errores de asyncpg; el código vive en orig o en su __cause__.
    orig = exc.orig
    code = getattr(orig, "pgcode", None)
    if code:
        return code
    cause = getattr(orig, "__cause__", None)
    return getattr(cause, "sqlstate", None)


class BaseRepository:
    """Base de los repos Postgres.

    Recibe la sesión compartida de la petición (la abre y commitea el UnitOfWork,
    no el repo) y traduce los errores de integridad de la base de datos a errores
    de dominio, para que el núcleo nunca vea excepciones de SQLAlchemy/asyncpg.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _flush(self, orm: object) -> None:
        try:
            await self.session.flush()
            await self.session.refresh(orm)
        except IntegrityError as exc:
            code = _pgcode(exc)
            if code == _UNIQUE_VIOLATION:
                raise DuplicateEntity() from exc
            if code == _FK_VIOLATION:
                raise ReferenceNotFound() from exc
            raise

    async def _delete(self, orm: object) -> None:
        try:
            await self.session.delete(orm)
            await self.session.flush()
        except IntegrityError as exc:
            if _pgcode(exc) == _FK_VIOLATION:
                raise EntityInUse() from exc
            raise
