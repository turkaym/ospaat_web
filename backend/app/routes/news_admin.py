# app/routes/news_admin.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import get_db_connection
from app.core.roles import require_role
from app.schemas.news import NewsCreate, NewsUpdate, NewsPublish
from app.services.news_service import (
    create_news,
    update_news,
    soft_delete_news,
    restore_news,
    set_publish_state,
)

router = APIRouter(prefix="/admin/news", tags=["Admin News"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_news_endpoint(
    data: NewsCreate,
    current_user=Depends(require_role("admin", "editor")),
):
    db = get_db_connection()
    news_id = create_news(db, current_user, data)
    db.close()

    return {"id": news_id}


@router.put("/{news_id}")
def update_news_endpoint(
    news_id: int,
    data: NewsUpdate,
    current_user=Depends(require_role("admin", "editor")),
):
    db = get_db_connection()
    updated = update_news(db, current_user, news_id, data)
    db.close()

    if not updated:
        raise HTTPException(status_code=404, detail="News not found")

    return {"message": "News updated"}


@router.delete("/{news_id}")
def delete_news_endpoint(
    news_id: int,
    current_user=Depends(require_role("admin", "editor")),
):
    db = get_db_connection()
    deleted = soft_delete_news(db, current_user, news_id)
    db.close()

    if not deleted:
        raise HTTPException(status_code=404, detail="News not found")

    return {"message": "News deleted"}


@router.post("/{news_id}/restore")
def restore_news_endpoint(
    news_id: int,
    current_user=Depends(require_role("admin", "editor")),
):
    db = get_db_connection()
    restored = restore_news(db, current_user, news_id)
    db.close()

    if not restored:
        raise HTTPException(status_code=404, detail="News not found")

    return {"message": "News restored"}


@router.patch("/{news_id}/publish")
def publish_news_endpoint(
    news_id: int,
    data: NewsPublish,
    current_user=Depends(require_role("admin", "editor")),
):
    db = get_db_connection()
    updated = set_publish_state(
        db, current_user, news_id, data.is_published
    )
    db.close()

    if not updated:
        raise HTTPException(status_code=404, detail="News not found")

    return {
        "message": "Published" if data.is_published else "Unpublished"
    }


@router.get("/")
def list_all_news_admin(
    page: int = 1,
    limit: int = 50,
    current_user=Depends(require_role("admin", "editor")),
):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    offset = (page - 1) * limit

    cursor.execute(
        """
        SELECT
            id,
            title,
            summary,
            content,
            is_published,
            is_deleted,
            created_at,
            published_at
        FROM news
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
        """,
        (limit, offset)
    )

    items = cursor.fetchall()

    cursor.close()
    db.close()

    return {
        "page": page,
        "limit": limit,
        "count": len(items),
        "items": items,
    }
