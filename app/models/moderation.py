import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, func, Float, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.db.base import Base


class ContentType(str, enum.Enum):
    TEXT = "text"
    IMAGE = "image"


class ModerationStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ModerationRequest(Base):
    __tablename__ = "moderation_requests"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[ContentType] = mapped_column(default=ContentType.TEXT)
    status: Mapped[ModerationStatus] = mapped_column(default=ModerationStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    company: Mapped["Company"] = relationship(back_populates="moderation_requests")
    result: Mapped["ModerationResult"] = relationship(back_populates="request")


class ModerationResult(Base):
    __tablename__ = "moderation_results"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("moderation_requests.id", ondelete="CASCADE"))
    is_toxic: Mapped[bool] = mapped_column(nullable=False)
    toxicity_score: Mapped[float] = mapped_column(Float, nullable=False)
    categories: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    request: Mapped["ModerationRequest"] = relationship(back_populates="result")