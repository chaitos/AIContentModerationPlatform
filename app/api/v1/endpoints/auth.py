from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_company
from app.crud.company import get_company_by_email, create_company
from app.crud.api_key import create_api_key, get_company_api_keys
from app.core.security import verify_password, create_access_token
from app.schemas.company import CompanyCreate, CompanyLogin, CompanyResponse
from app.schemas.api_key import ApiKeyResponse
from app.schemas.token import Token
from app.models.company import Company

router = APIRouter()


@router.post("/register", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def register(data: CompanyCreate, session: AsyncSession = Depends(get_db)):
    existing = await get_company_by_email(session, data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    company = await create_company(session, data)
    return company


@router.post("/login", response_model=Token)
async def login(data: CompanyLogin, session: AsyncSession = Depends(get_db)):
    company = await get_company_by_email(session, data.email)
    if not company or not verify_password(data.password, company.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token(subject=str(company.id))
    return Token(access_token=token)


@router.get("/me", response_model=CompanyResponse)
async def get_me(current_company: Company = Depends(get_current_company)):
    return current_company


@router.post("/api-keys", response_model=ApiKeyResponse, status_code=status.HTTP_201_CREATED)
async def generate_api_key(
    session: AsyncSession = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):
    api_key = await create_api_key(session, current_company.id)
    return api_key


@router.get("/api-keys", response_model=list[ApiKeyResponse])
async def list_api_keys(
    session: AsyncSession = Depends(get_db),
    current_company: Company = Depends(get_current_company),
):
    return await get_company_api_keys(session, current_company.id)