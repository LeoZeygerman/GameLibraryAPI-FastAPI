from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.genre import GenresOrm
from app.models.platform import PlatformsOrm

async def create_or_get_genre(session: AsyncSession, title: str) -> GenresOrm:
    genre = await session.scalar(
        select(GenresOrm)
        .where(GenresOrm.genre_title == title)
    )
    if genre is None:
        genre = GenresOrm(
            genre_title = title
        )
        session.add(genre)
        await session.flush()
    return genre


async def create_or_get_platform(session: AsyncSession, title: str):
    platform = await session.scalar(
        select(PlatformsOrm)
        .where(PlatformsOrm.platform_title == title)
    )
    if platform is None:
        platform = PlatformsOrm(
            platform_title = title
        )
        session.add()
        await session.flush()
    return platform
