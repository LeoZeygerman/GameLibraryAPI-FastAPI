from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.routers.game import router
from app.schemas.platform import ResponsePlatform, CreatePlatform, ResponsePlatformWithGames
from app.models.platform import PlatformsOrm
from app.database import SessionDep

@router.post('/platforms', summary='Добавить платформу', response_model=ResponsePlatform)
async def create_platform(session: SessionDep, platform = CreatePlatform):
    new_platform = PlatformsOrm(platform_title = platform.platform_title)
    session.add(new_platform)
    await session.commit()
    await session.refresh(new_platform)
    return new_platform

@router.get('/platforms/{platform_id}', summary='Получить платформу по ID', response_model=ResponsePlatformWithGames)
async def get_platform_by_id(session: SessionDep, platform_id: int):
    platform = await session.scalar(
        select(PlatformsOrm)
        .where(PlatformsOrm.id == platform_id)
        .options(selectinload(PlatformsOrm.games))
    )
    if platform is None:
        raise HTTPException(status_code=404, detail='Платформа не найдена!')
    return platform