from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exception import NotFoundError
from app.models.game import GamesOrm
from app.models.genre import GenresOrm
from app.schemas.genre import CreateGenre


async def get_genre_by_id(session: AsyncSession, genre_id: int):
    genre = await session.scalar(
        select(GenresOrm)
        .where(GenresOrm.id == genre_id)
        .options(
            selectinload(GenresOrm.games)
            .selectinload(GamesOrm.platform)
        )
    )
    if genre is None:
        raise NotFoundError(f'Жанр не найден!')
    return genre


async def get_all_genres(session: AsyncSession):
    genres = await session.scalars(
        select(GenresOrm)
    )
    return genres.all()


async def create_genre(session: AsyncSession, genre: CreateGenre):
    new_genre = GenresOrm(
        genre_title = genre.genre_title
    )
    session.add(new_genre)
    await session.flush()
    await session.commit()
    return new_genre


async def delete_genre(session: AsyncSession, genre_id: int):
    genre = await get_genre_by_id(session, genre_id)
    await session.delete(genre)
    await session.commit()
    return {f'Жанр удален!'}