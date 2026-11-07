import uuid
from typing import List, Optional, Tuple
from sqlalchemy import select, func, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.knowledge import KnowledgeArticle, ArticleBookmark
from app.repositories.base import BaseRepository


class KnowledgeRepository(BaseRepository[KnowledgeArticle]):
    def __init__(self, db: AsyncSession):
        super().__init__(KnowledgeArticle, db)

    async def list_articles(
        self,
        category: Optional[str] = None,
        search_query: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[KnowledgeArticle], int]:
        query = select(KnowledgeArticle).where(KnowledgeArticle.is_published.is_(True))
        count_query = select(func.count(KnowledgeArticle.id)).where(KnowledgeArticle.is_published.is_(True))

        if category:
            query = query.where(KnowledgeArticle.category.ilike(f"%{category}%"))
            count_query = count_query.where(KnowledgeArticle.category.ilike(f"%{category}%"))

        if search_query:
            term = f"%{search_query}%"
            filter_expr = or_(
                KnowledgeArticle.title_en.ilike(term),
                KnowledgeArticle.title_mr.ilike(term),
                KnowledgeArticle.title_hi.ilike(term),
                KnowledgeArticle.content_en.ilike(term),
            )
            query = query.where(filter_expr)
            count_query = count_query.where(filter_expr)

        total_res = await self.db.execute(count_query)
        total = total_res.scalar_one() or 0

        query = (
            query.order_by(desc(KnowledgeArticle.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        items_res = await self.db.execute(query)
        items = list(items_res.scalars().all())

        return items, total

    async def get_categories(self) -> List[str]:
        stmt = (
            select(KnowledgeArticle.category)
            .where(KnowledgeArticle.is_published.is_(True))
            .distinct()
        )
        res = await self.db.execute(stmt)
        return [row[0] for row in res.all() if row[0]]

    async def is_bookmarked(self, user_id: uuid.UUID, article_id: uuid.UUID) -> bool:
        stmt = select(ArticleBookmark).where(
            ArticleBookmark.user_id == user_id,
            ArticleBookmark.article_id == article_id,
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none() is not None

    async def toggle_bookmark(self, user_id: uuid.UUID, article_id: uuid.UUID) -> bool:
        stmt = select(ArticleBookmark).where(
            ArticleBookmark.user_id == user_id,
            ArticleBookmark.article_id == article_id,
        )
        res = await self.db.execute(stmt)
        bookmark = res.scalar_one_or_none()

        if bookmark:
            await self.db.delete(bookmark)
            await self.db.flush()
            return False  # Unbookmarked
        else:
            new_bookmark = ArticleBookmark(user_id=user_id, article_id=article_id)
            self.db.add(new_bookmark)
            await self.db.flush()
            return True  # Bookmarked
