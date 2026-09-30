from fastapi import APIRouter
from app.schemas.platform import *
from app.database import SessionDep
from app.services.platform import *

router = APIRouter(prefix='/platforms', tags=['Платформы'])

@router.post('/', summary='Добавить платформу', response_model=ResponsePlatform)
async def create_platform_router(session: SessionDep, platform: CreatePlatform):
    new_platform = await create_platform(session, platform)
    return new_platform


@router.get('/{platform_id}', summary='Получить платформу по ID', response_model=ResponsePlatformWithGames)
async def get_platform_by_id_router(session: SessionDep, platform_id: int):
    platform = await get_platform_by_id(session, platform_id)
    return platform


@router.get('/', summary='Получить все платформы', response_model=list[ResponsePlatform])
async def get_all_platforms_router(session: SessionDep):
    platforms = await get_all_platforms(session)
    return platforms


@router.delete('/{platform_id}', summary='Удалить платформу')
async def delete_platform_router(session: SessionDep, platform_id: int):
    platform = await delete_platform(session, platform_id)
    return platform