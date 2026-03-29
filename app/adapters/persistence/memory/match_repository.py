import uuid
from collections.abc import Sequence
from dataclasses import replace
from datetime import datetime, timezone

from adapters.persistence.memory.store import InMemoryStore
from core.domain.entities.match import Match
from core.domain.errors import EntityNotFound
from core.ports.outbound.match_repository import MatchRepository


class InMemoryMatchRepository(MatchRepository):
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    async def list(self, limit: int, offset: int) -> Sequence[Match]:
        all_matches = list(self.store.matches.values())
        return all_matches[offset : offset + limit]

    async def get(self, match_id: uuid.UUID) -> Match | None:
        return self.store.matches.get(match_id)

    async def add(self, match: Match) -> Match:
        persisted_match = replace(
            match, match_id=uuid.uuid4(), created_at=datetime.now(timezone.utc)
        )
        self.store.matches[persisted_match.match_id] = persisted_match
        return persisted_match

    async def update(self, match: Match) -> Match:
        if match.match_id not in self.store.matches:
            raise EntityNotFound(f"match not found: {match.match_id}")
        self.store.matches[match.match_id] = match
        return match
