import uuid
from datetime import datetime
from pydantic import BaseModel


class ApiKeyResponse(BaseModel):
    id: uuid.UUID
    key: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}