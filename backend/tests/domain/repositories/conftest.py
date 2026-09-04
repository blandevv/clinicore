"""Shared fixtures for domain repositories tests."""

import pytest

from src.domain.entities import BaseEntity


@pytest.fixture
def concrete_entity() -> BaseEntity:
    """Return a concrete BaseEntity for repository testing."""
    return BaseEntity()
