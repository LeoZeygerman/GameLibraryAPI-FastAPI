from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.routers.game import router
from app.database import SessionDep
from app.schemas.genre import CreateGenre, ResponseGenre, ResponseGenreWithGames
from app.models.genre import GenresOrm

@router.post('/new-genre', summary='Добавить новый жанр')
async def create_genre(session: SessionDep, genre: CreateGenre):
    new_genre = GenresOrm(genre_title = genre.genre_title)
    session.add(new_genre)
    await session.commit()
    return f'Жанр {genre.genre_title} добавлен!'


@router.get('/get-all-genres', summary='Получить список всех жанров', response_model=list[ResponseGenre])
async def get_all_genres(session: SessionDep):
    genres = await session.execute(
        select(GenresOrm)
    )
    return genres


@router.get('/get-genre-by-id/{genre_id}', summary='Получить жанр по ID', response_model=ResponseGenreWithGames)
async def get_genre_by_id(session: SessionDep, genre_id: int):
    genre = await session.scalar(
        select(GenresOrm)
        .where(GenresOrm.id == genre_id)
        .options(
            selectinload(GenresOrm.games)
        )
    )
    if genre is None:
        raise HTTPException(status_code=404, detail='Жанр не найден!')
    return genre