from app.core.database import get_db_connection
from datetime import datetime
from fastapi import APIRouter, Query, HTTPException
from typing import List
from app.models.news import get_published_news
from app.models.news import get_news_by_id

router = APIRouter(prefix="/news", tags=["News"])


@router.get("")
def list_news(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50)
):
    offset = (page - 1) * limit

    news = get_published_news(limit=limit, offset=offset)

    return {
        "page": page,
        "limit": limit,
        "count": len(news),
        "items": news
    }


@router.get("/{news_id}")
def get_news(news_id: int):
    news = get_news_by_id(news_id)

    if not news or not news.is_published:
        raise HTTPException(status_code=404, detail="News not found")

    return news


def create_news(title: str, summary: str, content: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO news (title, summary, content, is_published, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (title, summary, content, False, datetime.utcnow()),
    )

    conn.commit()
    news_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return news_id
