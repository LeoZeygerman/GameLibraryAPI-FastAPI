from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import GamesOrm
from app.exception import NotFoundError
from app.schemas.game import CreateGame
from app.services.lookups import create_or_get_genre, create_or_get_platform

async def get_game_by_name(session: AsyncSession, game_name:str) -> GamesOrm | None:
    result = await session.execute(
        select(GamesOrm)
        .where(GamesOrm.game_title == game_name)
        .options(
            selectinload(GamesOrm.platform),
            selectinload(GamesOrm.genres)
        )
    )
    return result.scalar_one_or_none()


async def delete_game_by_id(session: AsyncSession, game_id: int):
    query = await session.scalar(
        select(GamesOrm)
        .where(GamesOrm.id == game_id)
        .options(
            selectinload(GamesOrm.genres),
            selectinload(GamesOrm.platform)
        )
    )
    if query is None:
        raise NotFoundError(f'Игра не найдена!')
    await session.delete(query)
    await session.commit()


async def create_game(session: AsyncSession, game: CreateGame):
    platform = await create_or_get_platform(session, game.platform)

    genres = []
    for genre_title in game.genres:
        genre = await create_or_get_genre(session, genre_title)
        genres.append(genre)

    new_game = GamesOrm(
        game_title = game.game_title,
        description = game.description,
        release_year = game.release_year,
        platform = platform,
        genres = genres
    )
    session.add(new_game)
    await session.flush()
    await session.commit()
    return new_game