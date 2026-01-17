from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.core.database import get_db_connection


@dataclass
class User:
    id: int
    username: str
    password_hash: str
    role: str
    is_active: bool
    created_at: datetime


def get_user_by_username(username: str) -> Optional[User]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT id, username, password_hash, role, is_active, created_at
        FROM users
        WHERE username = %s
        LIMIT 1
    """

    cursor.execute(query, (username,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return None

    return User(**row)
