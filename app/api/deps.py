from typing import AsyncGenerator
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.core.security import decode_access_token
from app.crud.company import get_company_by_id, get_company_by_email
from app.crud.api_key import get_api_key
from app.models.company import Company

from fastapi import Header

bearer_scheme = HTTPBearer()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_company(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    session: AsyncSession = Depends(get_db),
) -> Company:
    token = credentials.credentials
    company_id = decode_access_token(token)

    if not company_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    company = await get_company_by_id(session, company_id)
    if not company or not company.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Company not found or inactive",
        )
    return company


async def get_company_by_api_key(
    session: AsyncSession = Depends(get_db),
    x_api_key: str = Header(...),
) -> Company:
    api_key = await get_api_key(session, x_api_key)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API key",
        )
    company = await get_company_by_id(session, api_key.company_id)
    if not company or not company.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Company not found or inactive",
        )
    return company