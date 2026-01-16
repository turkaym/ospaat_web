"""
JWT utilities for token encoding and decoding.

This module is intentionally framework-agnostic.
- No FastAPI
- No middleware
- No DB access

Defines the standard JWT behavior for the entire project.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import JWTError, jwt

# =========================
# JWT CONFIG
# =========================

JWT_ALGORITHM = "HS256"


def create_access_token(
    data: Dict[str, Any],
    secret_key: str,
    expires_minutes: int = 60,
) -> str:
    """
    Create a signed JWT access token.

    Args:
        data (dict): Payload data (e.g. {"sub": user_id, "role": "admin"})
        secret_key (str): Secret key used to sign the token
        expires_minutes (int): Token expiration time in minutes

    Returns:
        str: Encoded JWT token
    """
    if not secret_key:
        raise ValueError("Secret key must be provided")

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload["exp"] = expire

    token = jwt.encode(
        payload,
        secret_key,
        algorithm=JWT_ALGORITHM,
    )

    return token


def decode_access_token(
    token: str,
    secret_key: str,
) -> Dict[str, Any]:
    """
    Decode and validate a JWT access token.

    Args:
        token (str): JWT token string
        secret_key (str): Secret key used to sign the token

    Returns:
        dict: Decoded token payload

    Raises:
        JWTError: If token is invalid or expired
    """
    if not token or not secret_key:
        raise JWTError("Invalid token or secret key")

    payload = jwt.decode(
        token,
        secret_key,
        algorithms=[JWT_ALGORITHM],
    )

    return payload
