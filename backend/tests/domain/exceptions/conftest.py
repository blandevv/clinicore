"""Shared fixtures for domain exceptions tests."""

import pytest
from uuid import uuid4


@pytest.fixture
def sample_role_id():
    """Return a sample UUID for role operations."""
    return uuid4()


@pytest.fixture
def sample_role_name() -> str:
    """Return a sample role name."""
    return "admin"
