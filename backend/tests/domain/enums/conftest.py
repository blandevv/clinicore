"""Shared fixtures for domain enums tests."""

import pytest

from src.domain.enums import PermissionAction, PermissionResource


@pytest.fixture(params=list(PermissionAction), ids=lambda v: v.value)
def permission_action(request: pytest.FixtureRequest) -> PermissionAction:
    """Paremeterized fixture yielding each PermissionAction value."""
    return request.param


@pytest.fixture(params=list(PermissionResource), ids=lambda v: v.value)
def permission_resource(request: pytest.FixtureRequest) -> PermissionResource:
    """Paremeterized fixture yielding each PermissionResource value."""
    return request.param
