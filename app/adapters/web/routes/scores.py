import falcon.asgi

from adapters.web.resources.leaderboard_stream import LeaderboardStream
from adapters.web.resources.scores import GameLeaderboard, MatchScoreCollection
from core.ports.inbound.leaderboard_stream_use_case import LeaderboardStreamUseCase
from core.ports.inbound.score_use_case import ScoreUseCase


def register(
    app: falcon.asgi.App,
    score_use_case: ScoreUseCase,
    leaderboard_stream_use_case: LeaderboardStreamUseCase,
) -> None:
    app.add_route("/matches/{match_id}/scores", MatchScoreCollection(score_use_case))
    app.add_route("/games/{game_id}/leaderboard", GameLeaderboard(score_use_case))
    app.add_route(
        "/games/{game_id}/leaderboard/stream", LeaderboardStream(leaderboard_stream_use_case)
    )
