import uuid
from typing import List, Optional, Tuple
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.yield_prediction import YieldPrediction
from app.repositories.base import BaseRepository


class YieldRepository(BaseRepository[YieldPrediction]):
    def __init__(self, db: AsyncSession):
        super().__init__(YieldPrediction, db)

    async def list_for_user(
        self,
        user_id: Optional[uuid.UUID] = None,
        page: int = 1,
        page_size: int = 10,
        crop: Optional[str] = None
    ) -> Tuple[List[YieldPrediction], int]:
        query = select(YieldPrediction)
        count_query = select(func.count(YieldPrediction.id))

        if user_id:
            query = query.where(YieldPrediction.user_id == user_id)
            count_query = count_query.where(YieldPrediction.user_id == user_id)

        if crop:
            query = query.where(YieldPrediction.crop.ilike(f"%{crop}%"))
            count_query = count_query.where(YieldPrediction.crop.ilike(f"%{crop}%"))

        total_res = await self.db.execute(count_query)
        total = total_res.scalar_one() or 0

        query = (
            query.order_by(desc(YieldPrediction.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        items_res = await self.db.execute(query)
        items = list(items_res.scalars().all())

        return items, total
