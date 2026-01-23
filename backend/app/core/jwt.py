"""
JWT utilities for token encoding and decoding.

Framework-agnostic module:
- No FastAPI
- No DB
- No settings object

Uses environment variables only.
"""

import os
from datetime import datetime, timedelta
from typing import Any, Dict

from jose import JWTError, jwt


JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))


def create_access_token(
    subject: str,
    extra_claims: dict | None = None,
    expires_delta: timedelta | None = None
) -> str:
    to_encode = {
        "sub": subject,
        "iat": datetime.utcnow()
    }

    if extra_claims:
        to_encode.update(extra_claims)

    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=JWT_EXPIRE_MINUTES)
    )

    to_encode["exp"] = expire

    encoded_jwt = jwt.encode(
        to_encode,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    if not token:
        raise JWTError("Token is required")

    payload = jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
    )

    return payload
