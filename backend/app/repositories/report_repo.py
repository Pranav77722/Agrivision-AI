import uuid
from typing import List, Optional, Tuple
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.report import Report
from app.repositories.base import BaseRepository


class ReportRepository(BaseRepository[Report]):
    def __init__(self, db: AsyncSession):
        super().__init__(Report, db)

    async def get_with_diagnosis(self, report_id: uuid.UUID) -> Optional[Report]:
        stmt = (
            select(Report)
            .options(selectinload(Report.diagnosis))
            .where(Report.id == report_id)
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def list_for_user(
        self,
        user_id: Optional[uuid.UUID] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[Report], int]:
        query = select(Report)
        count_query = select(func.count(Report.id))

        if user_id:
            query = query.where(Report.user_id == user_id)
            count_query = count_query.where(Report.user_id == user_id)

        total_res = await self.db.execute(count_query)
        total = total_res.scalar_one() or 0

        query = (
            query.order_by(desc(Report.generated_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        items_res = await self.db.execute(query)
        items = list(items_res.scalars().all())

        return items, total
