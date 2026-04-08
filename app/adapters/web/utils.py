import uuid

import falcon


def parse_uuid(raw_value: str) -> uuid.UUID:
    try:
        return uuid.UUID(raw_value)
    except ValueError:
        raise falcon.HTTPBadRequest(description=f"invalid uuid: {raw_value}")
