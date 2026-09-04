"""Tests for src.domain.exceptions.domain_error module."""

from src.domain.exceptions import DomainError


class TestDomainError:
    """Tests for the DomainError base exception."""

    def test_is_exception(self) -> None:
        assert issubclass(DomainError, Exception)

    def test_has_default_code(self) -> None:
        assert DomainError.code == "domain_error"

    def test_init_with_detail_key(self) -> None:
        err = DomainError("some_key")
        assert err.detail_key == "some_key"
        assert err.context == {}

    def test_init_with_context(self) -> None:
        ctx = {"entity_id": "123"}
        err = DomainError("key", ctx)
        assert err.detail_key == "key"
        assert err.context == ctx

    def test_init_without_context(self) -> None:
        err = DomainError("key")
        assert err.context == {}

    def test_is_catchable_as_domain_error(self) -> None:
        try:
            raise DomainError("test")
        except DomainError as e:
            assert e.detail_key == "test"

    def test_is_catchable_as_exception(self) -> None:
        try:
            raise DomainError("test")
        except Exception:
            pass
