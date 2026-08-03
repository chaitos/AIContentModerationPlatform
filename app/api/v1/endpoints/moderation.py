import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_company_by_api_key
from app.crud.moderation import (
    create_moderation_request,
    get_moderation_request,
    get_company_requests,
)
from app.schemas.moderation import (
    ModerationRequestCreate,
    ModerationRequestResponse,
)
from app.tasks.moderation import process_moderation
from app.models.company import Company

router = APIRouter()


@router.post("/", response_model=ModerationRequestResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_content(
    data: ModerationRequestCreate,
    session: AsyncSession = Depends(get_db),
    company: Company = Depends(get_company_by_api_key),
):
    # Сохраняем запрос в БД
    request = await create_moderation_request(session, data, company.id)

    # Отправляем задачу в Celery — не ждём результата
    process_moderation.delay(str(request.id))

    return request


@router.get("/{request_id}", response_model=ModerationRequestResponse)
async def get_result(
    request_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    company: Company = Depends(get_company_by_api_key),
):
    request = await get_moderation_request(session, request_id, company.id)
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return request


@router.get("/", response_model=list[ModerationRequestResponse])
async def list_requests(
    limit: int = 20,
    offset: int = 0,
    session: AsyncSession = Depends(get_db),
    company: Company = Depends(get_company_by_api_key),
):
    return await get_company_requests(session, company.id, limit, offset)