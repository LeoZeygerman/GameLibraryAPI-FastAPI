from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.game import CreateGame
from app.models.platform import PlatformsOrm
from app.schemas.platform import CreatePlatform

async def get_platform_for_game(session: AsyncSession, platform: str):
    query = await session.execute(
        select(PlatformsOrm)
        .where(PlatformsOrm.platform_title == platform)
    )
    return query.scalar_one_or_none()


async def create_platform(session: AsyncSession, platform: str):
    query = PlatformsOrm(platform_title = platform)
    session.add(query)
    await session.flush()
    return query