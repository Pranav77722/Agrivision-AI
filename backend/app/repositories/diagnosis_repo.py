import uuid
from typing import List, Optional, Tuple
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.diagnosis import Diagnosis
from app.repositories.base import BaseRepository


class DiagnosisRepository(BaseRepository[Diagnosis]):
    def __init__(self, db: AsyncSession):
        super().__init__(Diagnosis, db)

    async def list_for_user(
        self,
        user_id: Optional[uuid.UUID] = None,
        page: int = 1,
        page_size: int = 10,
        crop_type: Optional[str] = None
    ) -> Tuple[List[Diagnosis], int]:
        query = select(Diagnosis)
        count_query = select(func.count(Diagnosis.id))

        if user_id:
            query = query.where(Diagnosis.user_id == user_id)
            count_query = count_query.where(Diagnosis.user_id == user_id)

        if crop_type:
            query = query.where(Diagnosis.crop_type.ilike(f"%{crop_type}%"))
            count_query = count_query.where(Diagnosis.crop_type.ilike(f"%{crop_type}%"))

        total_res = await self.db.execute(count_query)
        total = total_res.scalar_one() or 0

        query = (
            query.order_by(desc(Diagnosis.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        items_res = await self.db.execute(query)
        items = list(items_res.scalars().all())

        return items, total
