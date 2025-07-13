"""Base domain exceptions."""

class DomainException(Exception):
    """Base exception for all domain exceptions."""
    pass

class ValidationError(DomainException):
    """Raised when domain validation fails."""
    pass

class BusinessRuleViolation(DomainException):
    """Raised when a business rule is violated."""
    pass

class EntityNotFound(DomainException):
    """Raised when an entity is not found."""
    pass

class UnauthorizedError(DomainException):
    """Raised when an operation is not authorized."""
    pass

class ConflictError(DomainException):
    """Raised when there's a conflict with existing data."""
    pass
