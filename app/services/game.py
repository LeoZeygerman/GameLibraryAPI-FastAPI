from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import GamesOrm
from app.exception import NotFoundError
from app.schemas.game import CreateGame, UpdateGame
from app.services.lookups import create_or_get_genre, create_or_get_platform

async def get_game_by_name(session: AsyncSession, title:str) -> GamesOrm:
    game = await session.scalar(
        select(GamesOrm)
        .where(GamesOrm.game_title == title)
        .options(
            selectinload(GamesOrm.platform),
            selectinload(GamesOrm.genres)
        )
    )
    if game is None:
        raise NotFoundError(f'Игра {title} не найдена!')
    return game


async def delete_game_by_id(session: AsyncSession, game_id: int):
    game = await session.scalar(
        select(GamesOrm)
        .where(GamesOrm.id == game_id)
        .options(
            selectinload(GamesOrm.genres),
            selectinload(GamesOrm.platform)
        )
    )
    if game is None:
        raise NotFoundError(f'Игра не найдена!')
    await session.delete(game)
    await session.commit()
    return {'msg': 'Игра удалена!'}


async def create_game(session: AsyncSession, game: CreateGame) -> GamesOrm:
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


async def update_game(session: AsyncSession, title: str, data: UpdateGame) -> GamesOrm:
    game = await get_game_by_name(session, title)
    changes = data.model_dump(exclude_unset=True)
    await _apply_changes(session, game, changes)
    await session.flush()
    await session.commit()
    return game
    


async def _apply_platform(session: AsyncSession, game: GamesOrm, value: str):
    game.platform = await create_or_get_platform(session, value)


async def _apply_genres(session: AsyncSession, game: GamesOrm, value: list[str]):
    new_genres = []
    for title in value:
        genre = await create_or_get_genre(session, title)
        new_genres.append(genre)
    game.genres = new_genres


def _apply_simple(field: str):
    async def setter(session: AsyncSession, game: GamesOrm, value: str):
        setattr(game, field, value)
    return setter


_FIELD_HANDLERS = {
    'game_title': _apply_simple('game_title'),
    'description': _apply_simple('description'),
    'release_year': _apply_simple('release_year'),
    'platform': _apply_platform,
    'genres': _apply_genres
}


async def _apply_changes(session: AsyncSession, game: GamesOrm, changes: dict):
    for field, value in changes.items():
        handler = _FIELD_HANDLERS.get(field)
        if handler is None:
            raise NotFoundError(f'Передаваемый объект {field} не найден!')
        await handler(session, game, value)