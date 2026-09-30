from fastapi.responses import JSONResponse

from app.exception import AppException
import app.schemas
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
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


@app.exception_handler(AppException)
async def exception_handler(
    request: Request,
    exc: AppException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.detail}
    )

app.include_router(game_router)
app.include_router(genre_router)
app.include_router(platform_router)
