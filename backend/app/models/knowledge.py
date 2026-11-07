import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Text, Boolean, JSON, ForeignKey, DateTime, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class KnowledgeArticle(Base):
    __tablename__ = "knowledge_articles"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    category: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    title_en: Mapped[str] = mapped_column(String(255), nullable=False)
    title_mr: Mapped[str] = mapped_column(String(255), nullable=False)
    title_hi: Mapped[str] = mapped_column(String(255), nullable=False)
    content_en: Mapped[str] = mapped_column(Text, nullable=False)
    content_mr: Mapped[str] = mapped_column(Text, nullable=False)
    content_hi: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    bookmarks: Mapped[List["ArticleBookmark"]] = relationship(
        "ArticleBookmark", back_populates="article", cascade="all, delete-orphan"
    )


class ArticleBookmark(Base):
    __tablename__ = "article_bookmarks"
    __table_args__ = (
        UniqueConstraint("user_id", "article_id", name="uq_user_article_bookmark"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    article_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("knowledge_articles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    article: Mapped["KnowledgeArticle"] = relationship("KnowledgeArticle", back_populates="bookmarks")
