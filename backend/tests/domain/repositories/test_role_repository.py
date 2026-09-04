"""Tests for src.domain.repositories.role_repository module."""

from abc import ABC

import pytest

from src.domain.entities import RoleEntity
from src.domain.repositories import BaseRepository, RoleRepository


class TestRoleRepository:
    """Tests for the RoleRepository abstract class."""

    def test_is_abstract(self) -> None:
        assert issubclass(RoleRepository, ABC)

    def test_is_base_repository_subclass(self) -> None:
        assert issubclass(RoleRepository, BaseRepository)

    def test_cannot_be_instantiated(self) -> None:
        with pytest.raises(TypeError):
            RoleRepository()  # type: ignore[abstract]

    def test_has_list_roles_method(self) -> None:
        assert hasattr(RoleRepository, "list_roles")

    def test_has_exists_by_name_method(self) -> None:
        assert hasattr(RoleRepository, "exists_by_name")

    def test_has_find_by_name_method(self) -> None:
        assert hasattr(RoleRepository, "find_by_name")

    def test_incomplete_subclass_cannot_instantiate(self) -> None:
        class IncompleteRepo(RoleRepository):
            pass

        with pytest.raises(TypeError):
            IncompleteRepo()  # type: ignore[abstract]

    def test_complete_subclass_can_instantiate(self) -> None:
        class CompleteRepo(RoleRepository):
            async def find_by_id(self, entity_id):
                return None

            async def save(self, entity):
                pass

            async def list_roles(
                self, *, name=None, is_active=None, limit=10, offset=0
            ):
                return [], 0

            async def exists_by_name(self, name):
                return False

            async def find_by_name(self, name):
                return None

        repo = CompleteRepo()
        assert isinstance(repo, RoleRepository)
        assert isinstance(repo, BaseRepository)

    @pytest.mark.asyncio
    async def test_list_roles_returns_tuple(self) -> None:
        class MockRepo(RoleRepository):
            async def find_by_id(self, entity_id):
                return None

            async def save(self, entity):
                pass

            async def list_roles(
                self, *, name=None, is_active=None, limit=10, offset=0
            ):
                return [RoleEntity(name="admin")], 1

            async def exists_by_name(self, name):
                return False

            async def find_by_name(self, name):
                return None

        repo = MockRepo()
        roles, count = await repo.list_roles()
        assert len(roles) == 1
        assert count == 1

    @pytest.mark.asyncio
    async def test_exists_by_name_returns_bool(self) -> None:
        class MockRepo(RoleRepository):
            async def find_by_id(self, entity_id):
                return None

            async def save(self, entity):
                pass

            async def list_roles(
                self, *, name=None, is_active=None, limit=10, offset=0
            ):
                return [], 0

            async def exists_by_name(self, name):
                return name == "admin"

            async def find_by_name(self, name):
                return None

        repo = MockRepo()
        assert await repo.exists_by_name("admin") is True
        assert await repo.exists_by_name("other") is False

    @pytest.mark.asyncio
    async def test_find_by_name_returns_role_or_none(self) -> None:
        admin = RoleEntity(name="admin")

        class MockRepo(RoleRepository):
            async def find_by_id(self, entity_id):
                return None

            async def save(self, entity):
                pass

            async def list_roles(
                self, *, name=None, is_active=None, limit=10, offset=0
            ):
                return [], 0

            async def exists_by_name(self, name):
                return False

            async def find_by_name(self, name):
                return admin if name == "admin" else None

        repo = MockRepo()
        assert await repo.find_by_name("admin") is admin
        assert await repo.find_by_name("other") is None
