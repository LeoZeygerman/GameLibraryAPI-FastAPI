import app.schemas
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.platform import router as platform_router
from app.routers.game import router as game_router
from app.routers.genre import router as genre_router
from app.database import engine
from app.models.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(game_router)
app.include_router(genre_router)
app.include_router(platform_router)
