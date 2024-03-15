from core.database import init, teardown
from contextlib import asynccontextmanager


@asynccontextmanager
async def register():
    await init()
    yield
    await teardown()
