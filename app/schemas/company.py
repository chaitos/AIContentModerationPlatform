import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr


class CompanyCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class CompanyLogin(BaseModel):
    email: EmailStr
    password: str


class CompanyResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}