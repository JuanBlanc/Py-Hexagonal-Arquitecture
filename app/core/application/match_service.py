import uuid
from collections.abc import Sequence
from datetime import datetime, timezone

from core.domain.entities.match import Match
from core.domain.enums.match_status import MatchStatus
from core.domain.errors import EntityNotFound, IllegalStateTransition, ReferenceNotFound
from core.ports.inbound.match_use_case import MatchUseCase
from core.ports.outbound.unit_of_work import UnitOfWork, UnitOfWorkFactory


class MatchService(MatchUseCase):
    def __init__(self, unit_of_work: UnitOfWorkFactory) -> None:
        self._unit_of_work = unit_of_work

    async def create_match(self, game_id: uuid.UUID, host_player_id: uuid.UUID) -> Match:
        async with self._unit_of_work() as uow:
            game = await uow.games.get(game_id)
            if game is None:
                raise ReferenceNotFound(f"game not found: {game_id}")
            host_player = await uow.players.get(host_player_id)
            if host_player is None:
                raise ReferenceNotFound(f"host player not found: {host_player_id}")
            new_match = Match(
                game_id=game_id,
                host_player_id=host_player_id,
                status=MatchStatus.CREATED,
                player_ids=[host_player_id],
            )
            return await uow.matches.add(new_match)

    async def get_match(self, match_id: uuid.UUID) -> Match:
        async with self._unit_of_work() as uow:
            return await self._get_or_raise(uow, match_id)

    async def list_matches(self, limit: int, offset: int) -> Sequence[Match]:
        async with self._unit_of_work() as uow:
            return await uow.matches.list(limit, offset)

    async def start_match(self, match_id: uuid.UUID) -> Match:
        async with self._unit_of_work() as uow:
            match = await self._get_or_raise(uow, match_id)
            if match.status is not MatchStatus.CREATED:
                raise IllegalStateTransition(f"cannot start a match that is {match.status.value}")
            match.status = MatchStatus.IN_PROGRESS
            match.started_at = datetime.now(timezone.utc)
            return await uow.matches.update(match)

    async def finish_match(self, match_id: uuid.UUID) -> Match:
        async with self._unit_of_work() as uow:
            match = await self._get_or_raise(uow, match_id)
            if match.status is not MatchStatus.IN_PROGRESS:
                raise IllegalStateTransition(f"cannot finish a match that is {match.status.value}")
            match.status = MatchStatus.FINISHED
            match.finished_at = datetime.now(timezone.utc)
            return await uow.matches.update(match)

    async def abort_match(self, match_id: uuid.UUID) -> Match:
        async with self._unit_of_work() as uow:
            match = await self._get_or_raise(uow, match_id)
            if match.status in (MatchStatus.FINISHED, MatchStatus.ABORTED):
                raise IllegalStateTransition(f"cannot abort a match that is {match.status.value}")
            match.status = MatchStatus.ABORTED
            match.finished_at = datetime.now(timezone.utc)
            return await uow.matches.update(match)

    @staticmethod
    async def _get_or_raise(uow: UnitOfWork, match_id: uuid.UUID) -> Match:
        match = await uow.matches.get(match_id)
        if match is None:
            raise EntityNotFound(f"match not found: {match_id}")
        return match
