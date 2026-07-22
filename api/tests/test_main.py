import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_auth(client: AsyncClient, setup_db):
    response = await client.get('/')
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
