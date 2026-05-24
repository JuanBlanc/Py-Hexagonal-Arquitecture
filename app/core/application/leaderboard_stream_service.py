import uuid

from core.domain.leaderboard_subscription import LeaderboardSubscription
from core.ports.inbound.leaderboard_stream_use_case import LeaderboardStreamUseCase
from core.ports.outbound.leaderboard_publisher import LeaderboardPublisher


class LeaderboardStreamService(LeaderboardStreamUseCase):
    def __init__(self, leaderboard_publisher: LeaderboardPublisher) -> None:
        self.leaderboard_publisher = leaderboard_publisher

    def watch_leaderboard(self, game_id: uuid.UUID) -> LeaderboardSubscription:
        return self.leaderboard_publisher.open_subscription(game_id)
