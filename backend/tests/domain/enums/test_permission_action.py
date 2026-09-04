"""Tests for src.domain.enums.permission_action module."""

from enum import StrEnum

import pytest

from src.domain.enums import PermissionAction


class TestPermissionAction:
    """Tests for the PermissionAction enum."""

    def test_is_str_enum(self) -> None:
        assert issubclass(PermissionAction, StrEnum)

    @pytest.mark.parametrize(
        ("action", "expected_value"),
        [
            (PermissionAction.CREATE, "create"),
            (PermissionAction.READ, "read"),
            (PermissionAction.UPDATE, "update"),
            (PermissionAction.DELETE, "delete"),
            (PermissionAction.ACTIVATE, "activate"),
            (PermissionAction.DEACTIVATE, "deactivate"),
            (PermissionAction.ASSIGN, "assign"),
            (PermissionAction.UNASSIGN, "unassign"),
            (PermissionAction.CANCEL, "cancel"),
            (PermissionAction.RESCHEDULE, "reschedule"),
            (PermissionAction.CONFIRM, "confirm"),
        ],
    )
    def test_enum_value(self, action: PermissionAction, expected_value: str) -> None:
        assert action.value == expected_value

    def test_all_members_count(self) -> None:
        assert len(PermissionAction) == 11

    def test_member_names(self) -> None:
        expected = {
            "CREATE",
            "READ",
            "UPDATE",
            "DELETE",
            "ACTIVATE",
            "DEACTIVATE",
            "ASSIGN",
            "UNASSIGN",
            "CANCEL",
            "RESCHEDULE",
            "CONFIRM",
        }
        assert {m.name for m in PermissionAction} == expected

    def test_member_values_are_strings(self) -> None:
        for action in PermissionAction:
            assert isinstance(action, str)

    def test_member_is_hashable(self) -> None:
        assert hash(PermissionAction.CREATE) is not None
