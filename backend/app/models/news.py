from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.core.database import get_db_connection


@dataclass
class News:
    id: int
    title: str
    summary: Optional[str]
    content: str
    is_published: bool
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]


def get_published_news(limit: int = 10, offset: int = 0) -> list[News]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT id, title, summary, content,
               is_published, created_at, updated_at, published_at
        FROM news
        WHERE is_published = TRUE
        ORDER BY published_at DESC, created_at DESC
        LIMIT %s OFFSET %s
    """

    cursor.execute(query, (limit, offset))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [News(**row) for row in rows]


def get_news_by_id(news_id: int) -> Optional[News]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT id, title, summary, content,
               is_published, created_at, updated_at, published_at
        FROM news
        WHERE id = %s
        LIMIT 1
    """

    cursor.execute(query, (news_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return None

    return News(**row)
