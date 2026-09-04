"""Shared fixtures for domain value objects tests."""

import pytest

from src.domain.enums import PermissionAction, PermissionResource
from src.domain.value_objects import Permission


@pytest.fixture
def sample_permission() -> Permission:
    """Return a sample Permission value object."""
    return Permission(action=PermissionAction.READ, resource=PermissionResource.USER)
