"""Tests for src.domain.repositories.base_repository module."""

from abc import ABC
from uuid import uuid4

import pytest

from src.domain.entities import BaseEntity
from src.domain.repositories import BaseRepository


class TestBaseRepository:
    """Tests for the BaseRepository abstract class."""

    def test_is_abstract(self) -> None:
        assert issubclass(BaseRepository, ABC)

    def test_cannot_be_instantiated(self) -> None:
        with pytest.raises(TypeError):
            BaseRepository()  # type: ignore[abstract]

    def test_has_find_by_id_method(self) -> None:
        assert hasattr(BaseRepository, "find_by_id")

    def test_has_save_method(self) -> None:
        assert hasattr(BaseRepository, "save")

    def test_incomplete_subclass_cannot_instantiate(self) -> None:
        class IncompleteRepo(BaseRepository[BaseEntity]):
            pass

        with pytest.raises(TypeError):
            IncompleteRepo()  # type: ignore[abstract]

    def test_complete_subclass_can_instantiate(self) -> None:
        class CompleteRepo(BaseRepository[BaseEntity]):
            async def find_by_id(self, entity_id):
                return None

            async def save(self, entity):
                pass

        repo = CompleteRepo()
        assert isinstance(repo, BaseRepository)

    @pytest.mark.asyncio
    async def test_subclass_find_by_id_works(self) -> None:
        class MockRepo(BaseRepository[BaseEntity]):
            async def find_by_id(self, entity_id):
                return BaseEntity(entity_id=entity_id)

            async def save(self, entity):
                pass

        repo = MockRepo()
        entity_id = uuid4()
        result = await repo.find_by_id(entity_id)
        assert result is not None
        assert result.entity_id == entity_id

    @pytest.mark.asyncio
    async def test_subclass_save_works(self) -> None:
        saved = []

        class MockRepo(BaseRepository[BaseEntity]):
            async def find_by_id(self, entity_id):
                return None

            async def save(self, entity):
                saved.append(entity)

        repo = MockRepo()
        entity = BaseEntity()
        await repo.save(entity)
        assert saved == [entity]
