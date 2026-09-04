"""Tests for src.domain.entities.role_entity module."""

from uuid import UUID

import pytest

from src.domain.entities import AuditEntity, RoleEntity
from src.domain.enums import PermissionAction, PermissionResource
from src.domain.exceptions import RoleAlreadyDeletedError
from src.domain.value_objects import Permission


class TestRoleEntityCreation:
    """Tests for RoleEntity instantiation."""

    def test_is_audit_entity(self) -> None:
        assert issubclass(RoleEntity, AuditEntity)

    def test_creates_with_name(self, entity_id: UUID) -> None:
        role = RoleEntity(entity_id=entity_id, name="admin")
        assert role.name == "admin"
        assert role.entity_id == entity_id

    def test_default_description_none(self, entity_id: UUID) -> None:
        role = RoleEntity(entity_id=entity_id, name="admin")
        assert role.description is None

    def test_custom_description(self, entity_id: UUID) -> None:
        role = RoleEntity(entity_id=entity_id, name="admin", description="Full access")
        assert role.description == "Full access"

    def test_default_permissions_empty(self, entity_id: UUID) -> None:
        role = RoleEntity(entity_id=entity_id, name="admin")
        assert role.permissions == set()

    def test_default_is_active_true(self, entity_id: UUID) -> None:
        role = RoleEntity(entity_id=entity_id, name="admin")
        assert role.is_active is True

    def test_custom_permissions(self, role_entity_with_permissions: RoleEntity) -> None:
        assert len(role_entity_with_permissions.permissions) == 2

    def test_custom_is_active_false(self, entity_id: UUID) -> None:
        role = RoleEntity(entity_id=entity_id, name="admin", is_active=False)
        assert role.is_active is False


class TestHasPermission:
    """Tests for the has_permission method."""

    def test_returns_true_when_permission_exists(
        self, role_entity_with_permissions: RoleEntity
    ) -> None:
        perm = Permission(
            action=PermissionAction.READ, resource=PermissionResource.USER
        )
        assert role_entity_with_permissions.has_permission(perm) is True

    def test_returns_false_when_permission_missing(
        self, role_entity: RoleEntity
    ) -> None:
        perm = Permission(
            action=PermissionAction.READ, resource=PermissionResource.USER
        )
        assert role_entity.has_permission(perm) is False

    def test_returns_false_for_different_permission(
        self, role_entity_with_permissions: RoleEntity
    ) -> None:
        perm = Permission(
            action=PermissionAction.DELETE, resource=PermissionResource.USER
        )
        assert role_entity_with_permissions.has_permission(perm) is False


class TestGrantPermission:
    """Tests for the grant method."""

    def test_adds_permission(
        self, role_entity: RoleEntity, sample_permission: Permission
    ) -> None:
        role_entity.grant(sample_permission)
        assert sample_permission in role_entity.permissions

    def test_updates_timestamp(
        self, role_entity: RoleEntity, sample_permission: Permission
    ) -> None:
        old = role_entity.updated_at
        role_entity.grant(sample_permission)
        assert role_entity.updated_at >= old

    def test_granting_duplicate_is_idempotent(
        self, role_entity: RoleEntity, sample_permission: Permission
    ) -> None:
        role_entity.grant(sample_permission)
        role_entity.grant(sample_permission)
        assert len(role_entity.permissions) == 1

    def test_raises_when_deleted(
        self, entity_id: UUID, sample_permission: Permission
    ) -> None:
        role = RoleEntity(entity_id=entity_id, name="deleted")
        role.mark_deleted()
        with pytest.raises(RoleAlreadyDeletedError):
            role.grant(sample_permission)


class TestRevokePermission:
    """Tests for the revoke method."""

    def test_removes_permission(self, role_entity_with_permissions: RoleEntity) -> None:
        perm = Permission(
            action=PermissionAction.READ, resource=PermissionResource.USER
        )
        role_entity_with_permissions.revoke(perm)
        assert perm not in role_entity_with_permissions.permissions

    def test_discard_nonexistent_is_safe(self, role_entity: RoleEntity) -> None:
        perm = Permission(
            action=PermissionAction.READ, resource=PermissionResource.USER
        )
        role_entity.revoke(perm)
        assert len(role_entity.permissions) == 0

    def test_updates_timestamp(self, role_entity_with_permissions: RoleEntity) -> None:
        perm = Permission(
            action=PermissionAction.READ, resource=PermissionResource.USER
        )
        old = role_entity_with_permissions.updated_at
        role_entity_with_permissions.revoke(perm)
        assert role_entity_with_permissions.updated_at >= old

    def test_raises_when_deleted(self, entity_id: UUID) -> None:
        role = RoleEntity(entity_id=entity_id, name="deleted")
        role.mark_deleted()
        perm = Permission(
            action=PermissionAction.READ, resource=PermissionResource.USER
        )
        with pytest.raises(RoleAlreadyDeletedError):
            role.revoke(perm)


class TestActivate:
    """Tests for the activate method."""

    def test_sets_is_active_true(self, entity_id: UUID) -> None:
        role = RoleEntity(entity_id=entity_id, name="role", is_active=False)
        role.activate()
        assert role.is_active is True

    def test_updates_timestamp(self, entity_id: UUID) -> None:
        role = RoleEntity(entity_id=entity_id, name="role", is_active=False)
        old = role.updated_at
        role.activate()
        assert role.updated_at >= old

    def test_raises_when_deleted(self, entity_id: UUID) -> None:
        role = RoleEntity(entity_id=entity_id, name="role")
        role.mark_deleted()
        with pytest.raises(RoleAlreadyDeletedError):
            role.activate()


class TestDeactivate:
    """Tests for the deactivate method."""

    def test_sets_is_active_false(self, role_entity: RoleEntity) -> None:
        role_entity.deactivate()
        assert role_entity.is_active is False

    def test_updates_timestamp(self, role_entity: RoleEntity) -> None:
        old = role_entity.updated_at
        role_entity.deactivate()
        assert role_entity.updated_at >= old

    def test_raises_when_deleted(self, entity_id: UUID) -> None:
        role = RoleEntity(entity_id=entity_id, name="role")
        role.mark_deleted()
        with pytest.raises(RoleAlreadyDeletedError):
            role.deactivate()


class TestEnsureNotDeleted:
    """Tests for the _ensure_not_deleted guard."""

    def test_does_not_raise_when_not_deleted(self, role_entity: RoleEntity) -> None:
        role_entity._ensure_not_deleted()

    def test_raises_when_deleted(self, entity_id: UUID) -> None:
        role = RoleEntity(entity_id=entity_id, name="role")
        role.mark_deleted()
        with pytest.raises(RoleAlreadyDeletedError):
            role._ensure_not_deleted()
