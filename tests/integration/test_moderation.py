from unittest.mock import patch

import pytest
from httpx import AsyncClient


async def register_and_get_api_key(client: AsyncClient, email: str) -> str:
    """Хелпер — регистрирует компанию и возвращает API ключ."""
    await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test Co",
            "email": email,
            "password": "password123",
        },
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "password123",
        },
    )
    token = login.json()["access_token"]
    key_resp = await client.post(
        "/api/v1/auth/api-keys", headers={"Authorization": f"Bearer {token}"}
    )
    return key_resp.json()["key"]


@pytest.mark.asyncio
async def test_submit_moderation(client: AsyncClient):
    api_key = await register_and_get_api_key(client, "mod1@example.com")

    # Мокаем Celery чтобы не запускать реальный worker
    with patch("app.api.v1.endpoints.moderation.process_moderation.delay"):
        response = await client.post(
            "/api/v1/moderate/",
            json={"content": "Hello world", "content_type": "text"},
            headers={"x-api-key": api_key},
        )

    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "pending"
    assert data["content"] == "Hello world"


@pytest.mark.asyncio
async def test_submit_moderation_invalid_key(client: AsyncClient):
    response = await client.post(
        "/api/v1/moderate/",
        json={"content": "Hello", "content_type": "text"},
        headers={"x-api-key": "invalid-key"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_moderation_result(client: AsyncClient):
    api_key = await register_and_get_api_key(client, "mod2@example.com")

    with patch("app.api.v1.endpoints.moderation.process_moderation.delay"):
        create_resp = await client.post(
            "/api/v1/moderate/",
            json={"content": "Test content", "content_type": "text"},
            headers={"x-api-key": api_key},
        )

    request_id = create_resp.json()["id"]
    response = await client.get(
        f"/api/v1/moderate/{request_id}",
        headers={"x-api-key": api_key},
    )
    assert response.status_code == 200
    assert response.json()["id"] == request_id
