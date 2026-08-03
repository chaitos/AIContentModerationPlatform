from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.company import Company
from app.schemas.company import CompanyCreate
from app.core.security import hash_password


async def get_company_by_email(session: AsyncSession, email: str) -> Company | None:
    result = await session.execute(select(Company).where(Company.email == email))
    return result.scalar_one_or_none()


async def get_company_by_id(session: AsyncSession, company_id) -> Company | None:
    return await session.get(Company, company_id)


async def create_company(session: AsyncSession, data: CompanyCreate) -> Company:
    company = Company(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    session.add(company)
    await session.commit()
    await session.refresh(company)
    return company