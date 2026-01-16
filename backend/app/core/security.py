"""
Security utilities for password hashing and verification.

This module is intentionally framework-agnostic.
No DB, no FastAPI, no JWT usage here.
"""

from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        password (str): Plain text password.

    Returns:
        str: Hashed password.
    """
    if not password:
        raise ValueError("Password must not be empty")

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password (str): Plain text password.
        hashed_password (str): Stored hashed password.

    Returns:
        bool: True if match, False otherwise.
    """
    if not plain_password or not hashed_password:
        return False

    return pwd_context.verify(plain_password, hashed_password)
