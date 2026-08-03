import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.moderation import ContentType, ModerationStatus


class ModerationRequestCreate(BaseModel):
    content: str
    content_type: ContentType = ContentType.TEXT


class ModerationResultResponse(BaseModel):
    is_toxic: bool
    toxicity_score: float
    categories: dict
    created_at: datetime

    model_config = {"from_attributes": True}


class ModerationRequestResponse(BaseModel):
    id: uuid.UUID
    content: str
    content_type: ContentType
    status: ModerationStatus
    created_at: datetime
    result: ModerationResultResponse | None = None

    model_config = {"from_attributes": True}