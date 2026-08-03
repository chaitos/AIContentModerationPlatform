from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.api_key import ApiKey
import uuid


async def create_api_key(session: AsyncSession, company_id: uuid.UUID) -> ApiKey:
    api_key = ApiKey(company_id=company_id)
    session.add(api_key)
    await session.commit()
    await session.refresh(api_key)
    return api_key


async def get_api_key(session: AsyncSession, key: str) -> ApiKey | None:
    result = await session.execute(
        select(ApiKey).where(ApiKey.key == key, ApiKey.is_active == True)
    )
    return result.scalar_one_or_none()


async def get_company_api_keys(session: AsyncSession, company_id: uuid.UUID) -> list[ApiKey]:
    result = await session.execute(
        select(ApiKey).where(ApiKey.company_id == company_id)
    )
    return list(result.scalars().all())