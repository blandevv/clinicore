"""Tests for src.domain.entities.base_entity module."""

from uuid import UUID, uuid4

from src.domain.entities import BaseEntity


class TestBaseEntityCreation:
    """Tests for BaseEntity instantiation."""

    def test_creates_with_default_id(self) -> None:
        entity = BaseEntity()
        assert isinstance(entity.entity_id, UUID)

    def test_creates_with_explicit_id(self, entity_id: UUID) -> None:
        entity = BaseEntity(entity_id=entity_id)
        assert entity.entity_id == entity_id

    def test_two_entities_get_different_ids(self) -> None:
        e1 = BaseEntity()
        e2 = BaseEntity()
        assert e1.entity_id != e2.entity_id


class TestBaseEntityEquality:
    """Tests for BaseEntity __eq__."""

    def test_equal_same_id(self, entity_id: UUID) -> None:
        e1 = BaseEntity(entity_id=entity_id)
        e2 = BaseEntity(entity_id=entity_id)
        assert e1 == e2

    def test_not_equal_different_id(self) -> None:
        e1 = BaseEntity(entity_id=uuid4())
        e2 = BaseEntity(entity_id=uuid4())
        assert e1 != e2

    def test_not_equal_to_non_bas_entity(self, entity_id: UUID) -> None:
        entity = BaseEntity(entity_id=entity_id)
        assert entity != "not an entity"
        assert entity != 42
        assert entity != None  # noqa: E711

    def test_equal_with_itself(self, entity_id: UUID) -> None:
        entity = BaseEntity(entity_id=entity_id)
        assert entity == entity


class TestBaseEntityHash:
    """Tests for BaseEntity __hash__."""

    def test_hash_same_for_equal_entities(self, entity_id: UUID) -> None:
        e1 = BaseEntity(entity_id=entity_id)
        e2 = BaseEntity(entity_id=entity_id)
        assert hash(e1) == hash(e2)

    def test_hash_different_for_different_entities(self) -> None:
        e1 = BaseEntity(entity_id=uuid4())
        e2 = BaseEntity(entity_id=uuid4())
        assert hash(e1) != hash(e2)

    def test_usable_in_set(self, entity_id: UUID) -> None:
        e1 = BaseEntity(entity_id=entity_id)
        e2 = BaseEntity(entity_id=entity_id)
        assert len({e1, e2}) == 1

    def test_hash_includes_type(self) -> None:
        class SubEntity(BaseEntity):
            pass

        base = BaseEntity(entity_id=uuid4())
        sub = SubEntity(entity_id=base.entity_id)
        assert hash(base) != hash(sub)
