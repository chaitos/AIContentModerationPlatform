import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.moderation import ModerationRequest, ModerationStatus
from app.schemas.moderation import ModerationRequestCreate


async def create_moderation_request(
    session: AsyncSession,
    data: ModerationRequestCreate,
    company_id: uuid.UUID,
) -> ModerationRequest:
    from sqlalchemy.orm import selectinload
    request = ModerationRequest(
        company_id=company_id,
        content=data.content,
        content_type=data.content_type,
        status=ModerationStatus.PENDING,
    )
    session.add(request)
    await session.commit()

    result = await session.execute(
        select(ModerationRequest)
        .where(ModerationRequest.id == request.id)
        .options(selectinload(ModerationRequest.result))
    )
    return result.scalar_one()

async def get_moderation_request(
    session: AsyncSession,
    request_id: uuid.UUID,
    company_id: uuid.UUID,
) -> ModerationRequest | None:
    result = await session.execute(
        select(ModerationRequest)
        .where(
            ModerationRequest.id == request_id,
            ModerationRequest.company_id == company_id,
        )
        .options(selectinload(ModerationRequest.result))
    )
    return result.scalar_one_or_none()


async def get_company_requests(
    session: AsyncSession,
    company_id: uuid.UUID,
    limit: int = 20,
    offset: int = 0,
) -> list[ModerationRequest]:
    result = await session.execute(
        select(ModerationRequest)
        .where(ModerationRequest.company_id == company_id)
        .options(selectinload(ModerationRequest.result))
        .order_by(ModerationRequest.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all())