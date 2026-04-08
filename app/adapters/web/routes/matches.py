import falcon.asgi

from adapters.web.resources.matches import MatchCollection, MatchItem, MatchLifecycle
from core.ports.inbound.match_use_case import MatchUseCase


def register(app: falcon.asgi.App, match_use_case: MatchUseCase) -> None:
    app.add_route("/matches", MatchCollection(match_use_case))
    app.add_route("/matches/{match_id}", MatchItem(match_use_case))

    lifecycle = MatchLifecycle(match_use_case)
    app.add_route("/matches/{match_id}/start", lifecycle, suffix="start")
    app.add_route("/matches/{match_id}/finish", lifecycle, suffix="finish")
    app.add_route("/matches/{match_id}/abort", lifecycle, suffix="abort")
