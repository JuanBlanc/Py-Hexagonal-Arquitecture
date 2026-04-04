import asyncio
import uuid
from collections import defaultdict
from collections.abc import Callable

from core.domain.entities.score import Score
from core.domain.leaderboard_subscription import LeaderboardSubscription
from core.ports.outbound.leaderboard_publisher import LeaderboardPublisher


class InMemoryLeaderboardSubscription(LeaderboardSubscription):
    def __init__(self, score_queue: asyncio.Queue, on_close: Callable[[], None]) -> None:
        self.score_queue = score_queue
        self.on_close = on_close

    async def next_score(self) -> Score:
        return await self.score_queue.get()

    async def close(self) -> None:
        self.on_close()


class InMemoryLeaderboardPublisher(LeaderboardPublisher):
    def __init__(self) -> None:
        self.subscriber_queues_by_game: dict[uuid.UUID, list[asyncio.Queue]] = defaultdict(list)

    async def publish(self, score: Score) -> None:
        for score_queue in list(self.subscriber_queues_by_game.get(score.game_id, [])):
            await score_queue.put(score)

    def open_subscription(self, game_id: uuid.UUID) -> LeaderboardSubscription:
        score_queue: asyncio.Queue = asyncio.Queue()
        self.subscriber_queues_by_game[game_id].append(score_queue)

        def remove_queue() -> None:
            try:
                self.subscriber_queues_by_game[game_id].remove(score_queue)
            except ValueError:
                pass

        return InMemoryLeaderboardSubscription(score_queue, remove_queue)
