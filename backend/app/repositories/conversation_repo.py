import uuid
from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.conversation import Conversation, Message
from app.repositories.base import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, db: AsyncSession):
        super().__init__(Conversation, db)

    async def get_with_messages(self, conversation_id: uuid.UUID) -> Optional[Conversation]:
        stmt = (
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.id == conversation_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_for_user(
        self,
        user_id: Optional[uuid.UUID] = None,
        limit: int = 50
    ) -> List[Conversation]:
        stmt = (
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .order_by(desc(Conversation.created_at))
            .limit(limit)
        )
        if user_id:
            stmt = stmt.where(Conversation.user_id == user_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def add_message(
        self,
        conversation_id: uuid.UUID,
        role: str,
        content: str,
        audio_url: Optional[str] = None
    ) -> Message:
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            audio_url=audio_url,
        )
        self.db.add(msg)
        await self.db.flush()
        await self.db.refresh(msg)
        return msg
