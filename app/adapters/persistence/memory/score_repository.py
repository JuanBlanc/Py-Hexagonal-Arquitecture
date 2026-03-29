import uuid
from collections.abc import Sequence
from dataclasses import replace
from datetime import datetime, timezone

from adapters.persistence.memory.store import InMemoryStore
from core.domain.entities.score import Score
from core.ports.outbound.score_repository import ScoreRepository


class InMemoryScoreRepository(ScoreRepository):
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    async def add(self, score: Score) -> Score:
        persisted_score = replace(
            score, score_id=uuid.uuid4(), recorded_at=datetime.now(timezone.utc)
        )
        self.store.scores[persisted_score.score_id] = persisted_score
        return persisted_score

    async def list_for_match(self, match_id: uuid.UUID) -> Sequence[Score]:
        return [score for score in self.store.scores.values() if score.match_id == match_id]

    async def leaderboard_for_game(self, game_id: uuid.UUID, limit: int) -> Sequence[Score]:
        game_scores = [score for score in self.store.scores.values() if score.game_id == game_id]
        ranked_scores = sorted(game_scores, key=lambda score: score.points, reverse=True)
        return ranked_scores[:limit]
