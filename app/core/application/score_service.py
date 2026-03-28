import uuid
from collections.abc import Sequence

from core.domain.entities.score import Score
from core.domain.enums.match_status import MatchStatus
from core.domain.errors import IllegalStateTransition, ReferenceNotFound
from core.ports.inbound.score_use_case import ScoreUseCase
from core.ports.outbound.leaderboard_publisher import LeaderboardPublisher
from core.ports.outbound.unit_of_work import UnitOfWorkFactory


class ScoreService(ScoreUseCase):
    def __init__(
        self,
        unit_of_work: UnitOfWorkFactory,
        leaderboard_publisher: LeaderboardPublisher,
    ) -> None:
        self._unit_of_work = unit_of_work
        self.leaderboard_publisher = leaderboard_publisher

    async def submit_score(self, match_id: uuid.UUID, player_id: uuid.UUID, points: int) -> Score:
        async with self._unit_of_work() as uow:
            match = await uow.matches.get(match_id)
            if match is None:
                raise ReferenceNotFound(f"match not found: {match_id}")
            if match.status is not MatchStatus.IN_PROGRESS:
                raise IllegalStateTransition(
                    "scores are only accepted while the match is in progress"
                )
            submitted_score = Score(
                match_id=match_id,
                game_id=match.game_id,
                player_id=player_id,
                points=points,
            )
            recorded_score = await uow.scores.add(submitted_score)

        # Fuera de la transacción: solo se difunden puntuaciones ya confirmadas.
        await self.leaderboard_publisher.publish(recorded_score)
        return recorded_score

    async def list_match_scores(self, match_id: uuid.UUID) -> Sequence[Score]:
        async with self._unit_of_work() as uow:
            return await uow.scores.list_for_match(match_id)

    async def leaderboard(self, game_id: uuid.UUID, limit: int) -> Sequence[Score]:
        async with self._unit_of_work() as uow:
            return await uow.scores.leaderboard_for_game(game_id, limit)
