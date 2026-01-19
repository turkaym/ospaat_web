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
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]
    deleted_at: Optional[datetime]


def get_published_news(limit: int = 10, offset: int = 0) -> list[News]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT id, title, summary, content,
            is_published, is_deleted,
            created_at, updated_at, published_at, deleted_at
        FROM news
        WHERE is_published = TRUE
        AND is_deleted = FALSE
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
               is_published, is_deleted,
               created_at, updated_at, published_at, deleted_at
        FROM news
        WHERE id = %s
        AND is_deleted = FALSE
        LIMIT 1
    """

    cursor.execute(query, (news_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return None

    return News(**row)


def update_news(
    news_id: int,
    title: str | None = None,
    summary: str | None = None,
    content: str | None = None,
    is_published: bool | None = None,
) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    fields = []
    values = []

    if title is not None:
        fields.append("title = %s")
        values.append(title)

    if summary is not None:
        fields.append("summary = %s")
        values.append(summary)

    if content is not None:
        fields.append("content = %s")
        values.append(content)

    if is_published is not None:
        fields.append("is_published = %s")
        values.append(is_published)

        if is_published:
            fields.append("published_at = NOW()")
        else:
            fields.append("published_at = NULL")

    if not fields:
        return False

    values.append(news_id)

    query = f"""
        UPDATE news
        SET {", ".join(fields)}, updated_at = NOW()
        WHERE id = %s
        AND is_deleted = FALSE
    """

    cursor.execute(query, values)
    conn.commit()

    updated = cursor.rowcount > 0

    cursor.close()
    conn.close()

    return updated


def soft_delete_news(news_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE news
        SET is_deleted = TRUE,
            deleted_at = NOW(),
            is_published = FALSE,
            published_at = NULL,
            updated_at = NOW()
        WHERE id = %s
        AND is_deleted = FALSE
    """

    cursor.execute(query, (news_id,))
    conn.commit()

    deleted = cursor.rowcount > 0

    cursor.close()
    conn.close()

    return deleted


def create_news(
    title: str,
    content: str,
    summary: str | None,
    is_published: bool,
) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO news (title, summary, content, is_published, published_at)
        VALUES (%s, %s, %s, %s, %s)
    """

    published_at = datetime.utcnow() if is_published else None

    cursor.execute(
        query,
        (title, summary, content, is_published, published_at)
    )

    news_id = cursor.lastrowid

    conn.commit()
    cursor.close()
    conn.close()

    return news_id


def get_all_news(
    limit: int = 20,
    offset: int = 0
) -> list[News]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT id, title, summary, content,
               is_published, is_deleted,
               created_at, updated_at, published_at, deleted_at
        FROM news
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """

    cursor.execute(query, (limit, offset))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [News(**row) for row in rows]
