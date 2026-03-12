class DomainError(Exception):
    pass


class EntityNotFound(DomainError):
    pass


class DuplicateEntity(DomainError):
    pass


class ReferenceNotFound(DomainError):
    pass


class EntityInUse(DomainError):
    pass


class IllegalStateTransition(DomainError):
    pass
