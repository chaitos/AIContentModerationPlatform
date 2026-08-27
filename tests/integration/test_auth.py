import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test Company",
            "email": "test@example.com",
            "password": "testpassword123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test Company"
    assert "hashed_password" not in data  # пароль не утекает


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    payload = {
        "name": "Company",
        "email": "duplicate@example.com",
        "password": "password123",
    }
    await client.post("/api/v1/auth/register", json=payload)
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    # Сначала регистрируемся
    await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Login Test",
            "email": "login@example.com",
            "password": "password123",
        },
    )
    # Затем логинимся
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Company",
            "email": "wrongpass@example.com",
            "password": "correctpassword",
        },
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrongpass@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient):
    # Регистрация
    await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Me Company",
            "email": "me@example.com",
            "password": "password123",
        },
    )
    # Логин
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "me@example.com",
            "password": "password123",
        },
    )
    token = login_resp.json()["access_token"]

    # Запрос /me с токеном
    response = await client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"
