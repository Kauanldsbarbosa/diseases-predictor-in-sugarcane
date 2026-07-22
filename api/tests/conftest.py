import asyncio
import os

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient

from app.db.base import Base
from app.db.connection import Session, engine
from app.main import app

os.environ['ENVIRONMENT'] = 'test'
load_dotenv()


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db_session():
    async with Session() as session:
        try:
            yield session
        except Exception as e:
            print(f'Erro na sessão de teste: {e}')
        finally:
            try:
                await session.rollback()
            except Exception:
                pass
            await session.close()


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://localhost:8000'
    ) as c:
        yield c


@pytest.fixture
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = Session()
    yield session

    await session.close()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
