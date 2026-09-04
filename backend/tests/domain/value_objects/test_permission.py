"""Tests for src.domain.value_objects.permission module."""

import pytest

from src.domain.enums import PermissionAction, PermissionResource
from src.domain.value_objects import Permission


class TestPermissionCreation:
    """Tests for Permission instantiation."""

    def test_creates_permission(self) -> None:
        perm = Permission(
            action=PermissionAction.CREATE, resource=PermissionResource.PATIENT
        )
        assert perm.action == PermissionAction.CREATE
        assert perm.resource == PermissionResource.PATIENT

    def test_is_frozen(self) -> None:
        perm = Permission(
            action=PermissionAction.READ, resource=PermissionResource.USER
        )
        with pytest.raises(AttributeError):
            perm.action = PermissionAction.DELETE  # type: ignore[misc]


class TestPermissionValue:
    """Tests for the .value property."""

    @pytest.mark.parametrize(
        ("action", "resource", "expected"),
        [
            (PermissionAction.READ, PermissionResource.USER, "read:user"),
            (PermissionAction.CREATE, PermissionResource.PATIENT, "create:patient"),
            (PermissionAction.DELETE, PermissionResource.ROLE, "delete:role"),
            (PermissionAction.UPDATE, PermissionResource.DOCTOR, "update:doctor"),
            (
                PermissionAction.ASSIGN,
                PermissionResource.APPOINTMENT,
                "assign:appointment",
            ),
        ],
    )
    def test_value_property(
        self,
        action: PermissionAction,
        resource: PermissionResource,
        expected: str,
    ) -> None:
        perm = Permission(action=action, resource=resource)
        assert perm.value == expected


class TestPermissionStr:
    """Tests for __str__."""

    def test_str_returns_value(self) -> None:
        perm = Permission(
            action=PermissionAction.READ, resource=PermissionResource.USER
        )
        assert str(perm) == "read:user"

    def test_str_matches_value_property(self) -> None:
        perm = Permission(
            action=PermissionAction.CONFIRM, resource=PermissionResource.SURGERY
        )
        assert str(perm) == perm.value


class TestPermissionEquality:
    """Tests for equality based on frozen dataclass."""

    def test_same_action_and_resource_are_equal(self) -> None:
        p1 = Permission(action=PermissionAction.READ, resource=PermissionResource.USER)
        p2 = Permission(action=PermissionAction.READ, resource=PermissionResource.USER)
        assert p1 == p2

    def test_different_action_are_not_equal(self) -> None:
        p1 = Permission(action=PermissionAction.READ, resource=PermissionResource.USER)
        p2 = Permission(
            action=PermissionAction.DELETE, resource=PermissionResource.USER
        )
        assert p1 != p2

    def test_different_resource_are_not_equal(self) -> None:
        p1 = Permission(action=PermissionAction.READ, resource=PermissionResource.USER)
        p2 = Permission(action=PermissionAction.READ, resource=PermissionResource.ROLE)
        assert p1 != p2

    def test_is_hashable(self) -> None:
        p1 = Permission(action=PermissionAction.READ, resource=PermissionResource.USER)
        p2 = Permission(action=PermissionAction.READ, resource=PermissionResource.USER)
        assert hash(p1) == hash(p2)

    def test_usable_in_set(self) -> None:
        p1 = Permission(action=PermissionAction.READ, resource=PermissionResource.USER)
        p2 = Permission(action=PermissionAction.READ, resource=PermissionResource.USER)
        assert len({p1, p2}) == 1
