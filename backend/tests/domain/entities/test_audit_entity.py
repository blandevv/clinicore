"""Tests for src.domain.entities.audit_entity module."""

from datetime import UTC, datetime
from uuid import UUID

from src.domain.entities import AuditEntity, BaseEntity


class TestAuditEntityCreation:
    """Tests for AuditEntity instantiation."""

    def test_is_base_entity(self) -> None:
        assert issubclass(AuditEntity, BaseEntity)

    def test_default_timestamps_are_set(self, entity_id: UUID) -> None:
        entity = AuditEntity(entity_id=entity_id)
        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)

    def test_defaults_not_deleted(self, entity_id: UUID) -> None:
        entity = AuditEntity(entity_id=entity_id)
        assert entity.deleted_at is None
        assert entity.created_by is None
        assert entity.updated_by is None
        assert entity.deleted_by is None

    def test_is_not_deleted_by_default(self, audit_entity: AuditEntity) -> None:
        assert audit_entity.is_deleted is False


class TestIsDeletedProperty:
    """Tests for the is_deleted property."""

    def test_deleted_when_deleted_at_set(self, entity_id: UUID) -> None:
        entity = AuditEntity(entity_id=entity_id, deleted_at=datetime.now(UTC))
        assert entity.is_deleted is True

    def test_not_deleted_when_deleted_at_none(self, entity_id: UUID) -> None:
        entity = AuditEntity(entity_id=entity_id, deleted_at=None)
        assert entity.is_deleted is False


class TestMarkUpdated:
    """Tests for the mark_updated method."""

    def test_updates_timestamp(self, audit_entity: AuditEntity) -> None:
        old = audit_entity.updated_at
        audit_entity.mark_updated()
        assert audit_entity.updated_at >= old

    def test_sets_updated_by(self, audit_entity: AuditEntity, user_id: UUID) -> None:
        audit_entity.mark_updated(by=user_id)
        assert audit_entity.updated_by == user_id

    def test_updated_by_none_by_default(self, audit_entity: AuditEntity) -> None:
        audit_entity.mark_updated()
        assert audit_entity.updated_by is None

    def test_updated_at_is_utc(self, audit_entity: AuditEntity) -> None:
        audit_entity.mark_updated()
        assert audit_entity.updated_at.tzinfo is UTC


class TestMarkDeleted:
    """Tests for the mark_deleted method."""

    def test_sets_deleted_at(self, audit_entity: AuditEntity) -> None:
        audit_entity.mark_deleted()
        assert audit_entity.deleted_at is not None
        assert isinstance(audit_entity.deleted_at, datetime)

    def test_sets_deleted_by(self, audit_entity: AuditEntity, user_id: UUID) -> None:
        audit_entity.mark_deleted(by=user_id)
        assert audit_entity.deleted_by == user_id

    def test_is_deleted_after_mark(self, audit_entity: AuditEntity) -> None:
        audit_entity.mark_deleted()
        assert audit_entity.is_deleted is True

    def test_deleted_at_is_utc(self, audit_entity: AuditEntity) -> None:
        audit_entity.mark_deleted()
        assert audit_entity.deleted_at is not None
        assert audit_entity.deleted_at.tzinfo is UTC


class TestRestore:
    """Tests for the restore method."""

    def test_restores_deleted_at(self, audit_entity: AuditEntity) -> None:
        audit_entity.mark_deleted()
        audit_entity.restore()
        assert audit_entity.deleted_at is None

    def test_restores_deleted_by(
        self, audit_entity: AuditEntity, user_id: UUID
    ) -> None:
        audit_entity.mark_deleted(by=user_id)
        audit_entity.restore()
        assert audit_entity.deleted_by is None

    def test_not_deleted_after_restore(self, audit_entity: AuditEntity) -> None:
        audit_entity.mark_deleted()
        audit_entity.restore()
        assert audit_entity.is_deleted is False

    def test_restore_calls_mark_updated(
        self, audit_entity: AuditEntity, user_id: UUID
    ) -> None:
        audit_entity.mark_deleted()
        old = audit_entity.updated_at
        audit_entity.restore(by=user_id)
        assert audit_entity.updated_at >= old
        assert audit_entity.updated_by == user_id
