import falcon
import falcon.asgi

from core.domain.errors import (
    DomainError,
    DuplicateEntity,
    EntityInUse,
    EntityNotFound,
    IllegalStateTransition,
    ReferenceNotFound,
)


async def handle_not_found(req, resp, exception, params):
    resp.status = falcon.HTTP_404
    resp.media = {"error": str(exception)}


async def handle_conflict(req, resp, exception, params):
    resp.status = falcon.HTTP_409
    resp.media = {"error": str(exception)}


async def handle_unprocessable(req, resp, exception, params):
    resp.status = falcon.HTTP_422
    resp.media = {"error": str(exception)}


async def handle_unexpected(req, resp, exception, params):
    resp.status = falcon.HTTP_500
    resp.media = {"error": "unexpected error"}


def register_error_handlers(app: falcon.asgi.App) -> None:
    app.add_error_handler(EntityNotFound, handle_not_found)
    app.add_error_handler(DuplicateEntity, handle_conflict)
    app.add_error_handler(EntityInUse, handle_conflict)
    app.add_error_handler(IllegalStateTransition, handle_conflict)
    app.add_error_handler(ReferenceNotFound, handle_unprocessable)
    app.add_error_handler(DomainError, handle_unexpected)
