import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class ArticleBase(BaseModel):
    category: str = Field(..., min_length=2, max_length=100)
    title_en: str = Field(..., min_length=3, max_length=255)
    title_mr: str = Field(..., min_length=3, max_length=255)
    title_hi: str = Field(..., min_length=3, max_length=255)
    content_en: str = Field(..., min_length=10)
    content_mr: str = Field(..., min_length=10)
    content_hi: str = Field(..., min_length=10)
    tags: List[str] = Field(default_factory=list)
    is_published: bool = True


class ArticleCreate(ArticleBase):
    pass


class ArticleResponse(ArticleBase):
    id: uuid.UUID
    created_at: datetime
    is_bookmarked: bool = False

    model_config = ConfigDict(from_attributes=True)


class ArticleListResponse(BaseModel):
    items: List[ArticleResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class BookmarkResponse(BaseModel):
    success: bool
    bookmarked: bool
    article_id: uuid.UUID
    message: str
