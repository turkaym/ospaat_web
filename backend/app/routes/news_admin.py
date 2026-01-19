from app.schemas.news import NewsUpdate
from app.models.news import update_news
from fastapi import APIRouter, Depends, status, HTTPException

from app.core.roles import require_role
from app.models.news import create_news
from app.models.news import soft_delete_news
from app.models.news import get_all_news
from app.models.news import restore_news
from app.models.news import set_news_publish_state
from app.models.user import User
from app.schemas.news import NewsCreate
from app.schemas.news import NewsPublish

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


@router.delete("/{news_id}")
def delete_news_endpoint(
    news_id: int,
    current_user: User = Depends(require_role("admin", "editor")),
):
    deleted = soft_delete_news(news_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="News not found or already deleted"
        )

    return {
        "message": "News soft deleted",
        "news_id": news_id
    }


@router.get("/")
def list_all_news_admin(
    page: int = 1,
    limit: int = 20,
    current_user: User = Depends(require_role("admin", "editor")),
):
    offset = (page - 1) * limit

    news = get_all_news(limit=limit, offset=offset)

    return {
        "page": page,
        "limit": limit,
        "count": len(news),
        "items": news
    }


@router.post("/{news_id}/restore")
def restore_news_endpoint(
    news_id: int,
    current_user: User = Depends(require_role("admin", "editor")),
):
    restored = restore_news(news_id)

    if not restored:
        raise HTTPException(
            status_code=404,
            detail="News not found or not deleted"
        )

    return {
        "message": "News restored successfully",
        "news_id": news_id
    }


@router.patch("/{news_id}/publish")
def publish_news_endpoint(
    news_id: int,
    data: NewsPublish,
    current_user: User = Depends(require_role("admin", "editor")),
):
    updated = set_news_publish_state(
        news_id=news_id,
        is_published=data.is_published
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="News not found or already deleted"
        )

    return {
        "message": (
            "News published"
            if data.is_published
            else "News unpublished"
        ),
        "news_id": news_id
    }
