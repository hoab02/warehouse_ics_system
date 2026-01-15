class DomainError(Exception):
    pass

class InvalidStateTransition(DomainError):
    pass

class StationOccupied(DomainError):
    pass

class DuplicateTaskError(DomainError):
    pass

class InvalidSideMergeError(DomainError):
    pass
