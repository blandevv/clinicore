"""Tests for src.domain.enums.permission_resource module."""

from enum import StrEnum

import pytest

from src.domain.enums import PermissionResource


class TestPermissionResource:
    """Tests for the PermissionResource enum."""

    def test_is_str_enum(self) -> None:
        assert issubclass(PermissionResource, StrEnum)

    @pytest.mark.parametrize(
        ("resource", "expected_value"),
        [
            (PermissionResource.USER, "user"),
            (PermissionResource.ROLE, "role"),
            (PermissionResource.PERMISSION, "permission"),
            (PermissionResource.PATIENT, "patient"),
            (PermissionResource.NURSE, "nurse"),
            (PermissionResource.DOCTOR, "doctor"),
            (PermissionResource.SPECIALTY, "specialty"),
            (PermissionResource.APPOINTMENT, "appointment"),
            (PermissionResource.SURGERY, "surgery"),
            (PermissionResource.SURGERY_RESOURCE, "surgery_resource"),
            (PermissionResource.OPERATING_ROOM, "operating_room"),
        ],
    )
    def test_enum_value(
        self, resource: PermissionResource, expected_value: str
    ) -> None:
        assert resource.value == expected_value

    def test_all_members_count(self) -> None:
        assert len(PermissionResource) == 11

    def test_member_names(self) -> None:
        expected = {
            "USER",
            "ROLE",
            "PERMISSION",
            "PATIENT",
            "NURSE",
            "DOCTOR",
            "SPECIALTY",
            "APPOINTMENT",
            "SURGERY",
            "SURGERY_RESOURCE",
            "OPERATING_ROOM",
        }
        assert {m.name for m in PermissionResource} == expected

    def test_member_values_are_strings(self) -> None:
        for resource in PermissionResource:
            assert isinstance(resource, str)

    def test_member_is_hashable(self) -> None:
        assert hash(PermissionResource.USER) is not None
