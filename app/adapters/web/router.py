import falcon.asgi

from adapters.web.lifespan import LifespanMiddleware
from adapters.web.routes import games, health, matches, matchmaking, players, scores
from composition import CompositionRoot


def create_app(composition: CompositionRoot) -> falcon.asgi.App:
    app = falcon.asgi.App(
        middleware=[LifespanMiddleware(composition.startup, composition.shutdown)]
    )

    health.register(app)
    players.register(app, composition.player_use_case)
    games.register(app, composition.game_use_case)
    matches.register(app, composition.match_use_case)
    scores.register(app, composition.score_use_case, composition.leaderboard_stream_use_case)
    matchmaking.register(app, composition.matchmaking_use_case)

    return app
