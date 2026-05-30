from collections.abc import Awaitable, Callable
from typing import Any

Hook = Callable[[], Awaitable[None]]


class LifespanMiddleware:
    """Middleware ASGI que engancha arranque/apagado de Falcon a hooks de la app.

    Mantiene el ciclo de vida de los recursos (p.ej. el engine de Postgres) en el
    borde driving: el núcleo no sabe nada de esto.
    """

    def __init__(self, on_startup: Hook | None = None, on_shutdown: Hook | None = None) -> None:
        self._on_startup = on_startup
        self._on_shutdown = on_shutdown

    async def process_startup(self, scope: dict[str, Any], event: dict[str, Any]) -> None:
        if self._on_startup is not None:
            await self._on_startup()

    async def process_shutdown(self, scope: dict[str, Any], event: dict[str, Any]) -> None:
        if self._on_shutdown is not None:
            await self._on_shutdown()
