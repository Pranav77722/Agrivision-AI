import uuid
import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_optional, get_current_user
from app.models.user import User
from app.repositories.knowledge_repo import KnowledgeRepository
from app.schemas.knowledge import ArticleResponse, ArticleListResponse, BookmarkResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/knowledge", tags=["Agricultural Knowledge Base"])


@router.get(
    "/categories",
    response_model=List[str],
    summary="List article categories",
    description="Retrieve all available article categories (e.g. Disease Management, Soil & Fertilizers, Crop Protection, Modern Farming)."
)
async def get_categories(db: AsyncSession = Depends(get_db)) -> List[str]:
    repo = KnowledgeRepository(db)
    return await repo.get_categories()


@router.get(
    "/",
    response_model=ArticleListResponse,
    summary="List agricultural knowledge articles",
    description="Browse and search published agronomic articles with category filtering and keyword search."
)
async def list_articles(
    category: Optional[str] = Query(None, description="Category filter"),
    q: Optional[str] = Query(None, description="Search keyword"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
) -> ArticleListResponse:
    repo = KnowledgeRepository(db)
    items, total = await repo.list_articles(
        category=category,
        search_query=q,
        page=page,
        page_size=page_size
    )

    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    # Check bookmark status if user is authenticated
    resp_items = []
    for item in items:
        art_resp = ArticleResponse.model_validate(item)
        if current_user:
            art_resp.is_bookmarked = await repo.is_bookmarked(current_user.id, item.id)
        resp_items.append(art_resp)

    return ArticleListResponse(
        items=resp_items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get(
    "/{id}",
    response_model=ArticleResponse,
    summary="Get article detail",
    description="Retrieve full content of a specific knowledge base article."
)
async def get_article(
    id: uuid.UUID,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
) -> ArticleResponse:
    repo = KnowledgeRepository(db)
    article = await repo.get(id)
    if not article or not article.is_published:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge article not found.",
        )

    resp = ArticleResponse.model_validate(article)
    if current_user:
        resp.is_bookmarked = await repo.is_bookmarked(current_user.id, article.id)
    return resp


@router.post(
    "/bookmark/{id}",
    response_model=BookmarkResponse,
    summary="Bookmark or unbookmark article",
    description="Toggle bookmark status for a knowledge article."
)
async def toggle_bookmark(
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> BookmarkResponse:
    repo = KnowledgeRepository(db)
    article = await repo.get(id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found.",
        )

    is_now_bookmarked = await repo.toggle_bookmark(current_user.id, id)
    msg = "Article bookmarked." if is_now_bookmarked else "Article bookmark removed."

    return BookmarkResponse(
        success=True,
        bookmarked=is_now_bookmarked,
        article_id=id,
        message=msg
    )
