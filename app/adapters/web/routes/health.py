import falcon.asgi

from adapters.web.resources.health import HealthResource


def register(app: falcon.asgi.App) -> None:
    app.add_route("/health", HealthResource())
