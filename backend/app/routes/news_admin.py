from app.schemas.news import NewsUpdate
from app.models.news import update_news
from fastapi import APIRouter, Depends, status, HTTPException

from app.core.roles import require_role
from app.models.news import create_news
from app.models.user import User
from app.schemas.news import NewsCreate


router = APIRouter(prefix="/admin/news", tags=["Admin News"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_news_endpoint(
    data: NewsCreate,
    current_user: User = Depends(require_role("admin", "editor")),
):
    news_id = create_news(
        title=data.title,
        summary=data.summary,
        content=data.content,
        is_published=data.is_published,
    )

    return {
        "message": "News created",
        "news_id": news_id,
    }


@router.put("/{news_id}")
def update_news_endpoint(
    news_id: int,
    data: NewsUpdate,
    current_user: User = Depends(require_role("admin", "editor")),
):
    updated = update_news(
        news_id=news_id,
        title=data.title,
        summary=data.summary,
        content=data.content,
        is_published=data.is_published,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="News not found or no changes applied"
        )

    return {
        "message": "News updated successfully",
        "news_id": news_id
    }
