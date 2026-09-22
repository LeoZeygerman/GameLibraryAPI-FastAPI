from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import SessionDep
from app.schemas.game import CreateGame, ResponseGame, UpdateGame
from app.models.game import GamesOrm
from app.models.platform import PlatformsOrm
from app.models.genre import GenresOrm

router = APIRouter(prefix='/games', tags=['Игры'])

@router.post('/', summary='Добавить игру', response_model=ResponseGame)
async def create_game(session: SessionDep, game: CreateGame):
    platform = await session.scalar(
        select(PlatformsOrm)
        .where(PlatformsOrm.platform_title == game.platform)
    )
    if platform is None:
        platform = PlatformsOrm(
                platform_title = game.platform
            )
        session.add(platform)
        await session.flush()

    genres = []
    for genre_title in game.genre:
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
        genres.append(genre)

    new_game = GamesOrm(
            game_title = game.game_title,
            description = game.description,
            release_year = game.release_year,
            platform = platform,
            genres = genres
        )
    
    session.add(new_game)
    await session.commit()

    result = await session.execute(
        select(GamesOrm)
        .where(GamesOrm.id == new_game.id)
        .options(
            selectinload(GamesOrm.genres),
            selectinload(GamesOrm.platform)
            )
    )
    return result.scalar_one()


@router.get('/get-by-name/{game_name}', summary='Получить игру по названию', response_model=ResponseGame)
async def get_game_by_name(session: SessionDep, game_name: str):
    result = await session.execute(
        select(GamesOrm)
        .where(GamesOrm.game_title == game_name)
        .options(
            selectinload(GamesOrm.genres),
            selectinload(GamesOrm.platform)
        )
    )
    game = result.scalar_one_or_none()
    if not game:
        raise HTTPException(status_code=404, detail='Игра не найдена!')
    return game


@router.patch('/update/{game_name}', summary='Изменить игру', response_model=ResponseGame)
async def update_game(session: SessionDep, game_name: str, game: UpdateGame):
    query = await session.execute(
        select(GamesOrm)
        .where(GamesOrm.game_title == game_name)
        .options(
            selectinload(GamesOrm.genres),
            selectinload(GamesOrm.platform)
        )
    )
    result = query.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail='Игра не найдена!')
    changes = game.model_dump(exclude_unset=True)

    simple_fields = ['game_title', 'description', 'release_year']
    for field in simple_fields:
        if field in changes:
            setattr(result, field, changes[field])

    if 'platform' in changes:
        platform_title_changes = changes['platform']
        query = await session.scalar(
            select(PlatformsOrm)
            .where(PlatformsOrm.platform_title == platform_title_changes)
        )
        if query is None:
            query = PlatformsOrm(
                platform_title = platform_title_changes
            )
            session.add(query)
            await session.flush()
        result.platform = query

    if 'genres' in changes:
        new_genres = []
        for new_genre_title in changes['genres']:
            genre = await session.scalar(
                select(GenresOrm)
                .where(GenresOrm.genre_title == new_genre_title)
            )
            if genre is None:
                genre = GenresOrm(
                    genre_title = new_genre_title
                )
                session.add(genre)
                await session.flush()
            new_genres.append(genre)
        result.genres = new_genres


@router.delete('/delete/{game_id}', summary='Удалить игру')
async def delete_game(session: SessionDep, game_id: int):
    game = await session.scalar(
        select(GamesOrm)
        .where(GamesOrm.id == game_id)
        .options(
            selectinload(GamesOrm.genres),
            selectinload(GamesOrm.platform)
        )
    )
    if game is None:
        raise HTTPException(status_code=404, detail='Игра не найдена!')
    session.delete(game)
    await session.commit()
    return f'Игра удалена!'
