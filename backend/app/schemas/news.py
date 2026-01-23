from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NewsCreate(BaseModel):
    title: str
    summary: Optional[str] = None
    content: str
    is_published: bool = False


class NewsUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    summary: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = None
    is_published: Optional[bool] = None


class NewsResponse(BaseModel):
    id: int
    title: str
    summary: Optional[str]
    content: str
    is_published: bool
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]

    class Config:
        from_attributes = True


class NewsPublish(BaseModel):
    is_published: bool
