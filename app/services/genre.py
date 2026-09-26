from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.game import CreateGame
from app.models.genre import GenresOrm
from app.schemas.genre import CreateGenre

async def get_genre_for_game(session: AsyncSession, genre: CreateGame) -> GenresOrm | None:
    return await session.scalar(
        select(GenresOrm)
        .where(genre_title = genre)
    )


async def create_genre(session: AsyncSession, genre: CreateGenre):
    query = GenresOrm(genre_title = genre.genre_title)
    await session.add(query)
    await session.flush()