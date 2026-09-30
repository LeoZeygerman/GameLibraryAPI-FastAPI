from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exception import NotFoundError
from app.models.platform import PlatformsOrm
from app.schemas.platform import CreatePlatform

async def get_platform_by_id(session: AsyncSession, platform_id: int) -> PlatformsOrm:
    platform = await session.scalar(
        select(PlatformsOrm)
        .where(PlatformsOrm.id == platform_id)
        .options(selectinload(
            PlatformsOrm.games
        ))
    )
    if platform is None:
        raise NotFoundError(f'Платформа с таким ID не найдена')
    return platform


async def get_all_platforms(session: AsyncSession) -> list[PlatformsOrm]:
    platforms = await session.scalars(
        select(PlatformsOrm)
    )
    return platforms.all()


async def create_platform(session: AsyncSession, platform: CreatePlatform) -> PlatformsOrm:
    new_platform = (
        PlatformsOrm(
            platform_title = platform.platform_title
        )
    )
    session.add(new_platform)
    await session.commit()
    return new_platform


async def delete_platform(session: AsyncSession, platform_id: int):
    platform = get_platform_by_id(session, platform_id)
    await session.delete(platform)
    await session.commit()
    return f'Платформа удалена!'