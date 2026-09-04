"""Provide password hashing and JWT token utilities."""

from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from src.core.config import settings


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(
    subject: str | int, extra_data: dict[str, object] | None = None
) -> str:
    """Create a JWT access token for the specified subject."""
    now = datetime.now(UTC)

    payload: dict[str, object] = {
        "sub": str(subject),
        "type": "access",
        "iss": "clinicore-api",
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt_access_token_expire_minutes),
    }

    if extra_data:
        payload.update(extra_data)

    return jwt.encode(  # pyright: ignore[reportUnknownMemberType]
        payload,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token(subject: str | int) -> str:
    """Create a JWT refresh token for the specified subject."""
    now = datetime.now(UTC)

    payload: dict[str, object] = {
        "sub": str(subject),
        "type": "refresh",
        "iss": "clinicore-api",
        "iat": now,
        "exp": now + timedelta(days=settings.jwt_refresh_token_expire_days),
    }

    return jwt.encode(  # pyright: ignore[reportUnknownMemberType]
        payload,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )


class InvalidTokenTypeError(Exception):
    """Raised when a JWT token has an unexpected type."""

    ...


def _decode_token(token: str, expected_type: str) -> dict[str, object]:
    """Decode and validate a JWT token with the expected type."""
    payload = jwt.decode(  # pyright: ignore[reportUnknownMemberType]
        token,
        settings.jwt_secret_key.get_secret_value(),
        algorithms=[settings.jwt_algorithm],
        issuer="clinicore-api",
    )
    if payload.get("type") != expected_type:
        raise InvalidTokenTypeError(expected_type)
    return payload


def decode_access_token(token: str) -> dict[str, object]:
    """Decode and validate an access token."""
    return _decode_token(token, "access")


def decode_refresh_token(token: str) -> dict[str, object]:
    """Decode and validate a refresh token."""
    return _decode_token(token, "refresh")
