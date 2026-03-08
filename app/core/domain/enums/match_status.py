from enum import Enum


class MatchStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    ABORTED = "aborted"
