from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.genre import GenresOrm

async def create_or_get_genre(session: AsyncSession, genre_title: str) -> GenresOrm:
    genre = await session.scalar(
        select(GenresOrm)
        .where(GenresOrm.genre_title == genre_title)
    )
    if genre is None:
        genre = GenresOrm(
            genre_title = genre_title
        )
        session.add(genre)
        await session.flush()
    return genre