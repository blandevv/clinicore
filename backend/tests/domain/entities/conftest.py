"""Shared fixtures for domain entities tests."""

from uuid import UUID, uuid4

import pytest

from src.domain.entities import AuditEntity, BaseEntity, RoleEntity
from src.domain.enums import PermissionAction, PermissionResource
from src.domain.value_objects import Permission


@pytest.fixture
def entity_id() -> UUID:
    """Fixture to generate a unique entity ID."""
    return uuid4()


@pytest.fixture
def base_entity(entity_id: UUID) -> BaseEntity:
    """Return a BaseEntity with a known ID."""
    return BaseEntity(entity_id=entity_id)


@pytest.fixture
def audit_entity(entity_id: UUID) -> AuditEntity:
    """Return an AuditEntity with a known ID."""
    return AuditEntity(entity_id=entity_id)


@pytest.fixture
def user_id() -> UUID:
    """Return a UUID representing a user performing actions."""
    return uuid4()


@pytest.fixture
def sample_permission() -> Permission:
    """Return a sample Permission value object."""
    return Permission(action=PermissionAction.READ, resource=PermissionResource.USER)


@pytest.fixture
def role_entity(entity_id: UUID) -> RoleEntity:
    """Return a RoleEntity with default values."""
    return RoleEntity(entity_id=entity_id, name="admin")


@pytest.fixture
def role_entity_with_permissions(entity_id: UUID) -> RoleEntity:
    """Return a RoleEntity with pre-assigned permissions."""
    perms = {
        Permission(action=PermissionAction.READ, resource=PermissionResource.USER),
        Permission(action=PermissionAction.CREATE, resource=PermissionResource.PATIENT),
    }
    return RoleEntity(entity_id=entity_id, name="doctor", permissions=perms)
