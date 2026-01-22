class DomainError(Exception):
    pass

class InvalidStateTransition(DomainError):
    pass

class ScenarioValidationException(DomainError):
    pass

class InvalidTaskOrderError(DomainError):
    pass

class ScenarioAlreadyExistsException(DomainError):
    pass

