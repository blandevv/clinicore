"""Shared fixtures for domain entities tests."""

from uuid import UUID, uuid4

import pytest

from src.domain.entities import AuditEntity, BaseEntity


@pytest.fixture
def entity_id() -> UUID:
    """Fixture to generate a unique entity ID."""
    return uuid4()


@pytest.fixture
def base_entity(entity_id: UUID) -> BaseEntity:
    """Return a BaseEntity instance with a unique entity ID."""
    return BaseEntity(entity_id=entity_id)


@pytest.fixture
def user_id() -> UUID:
    """Return a UUID representing a user performing actions."""
    return uuid4()


@pytest.fixture
def audit_entity(entity_id: UUID) -> AuditEntity:
    """Return an AuditEntity instance with a unique entity ID."""
    return AuditEntity(entity_id=entity_id)
