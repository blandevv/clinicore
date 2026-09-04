"""Expose domain exceptions for package-level imports."""

from .domain_error import DomainError
from .role_errors import (
    RoleAlreadyDeletedError,
    RoleAlreadyExistsError,
    RoleNotFoundError,
)

__all__ = [
    "DomainError",
    "RoleAlreadyDeletedError",
    "RoleAlreadyExistsError",
    "RoleNotFoundError",
]
