from fastapi import HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import SessionDep
from app.schemas.genre import CreateGenre, ResponseGenre, ResponseGenreWithGames
from app.models.genre import GenresOrm

router = APIRouter(prefix='/genres', tags=['Жанры'])

@router.post('/genres', summary='Добавить новый жанр', response_model=ResponseGenre)
async def create_genre(session: SessionDep, genre: CreateGenre):
    new_genre = GenresOrm(genre_title = genre.genre_title)
    session.add(new_genre)
    await session.commit()
    await session.refresh(new_genre)
    return new_genre


@router.get('/genres', summary='Получить список всех жанров', response_model=list[ResponseGenre])
async def get_all_genres(session: SessionDep):
    genres = await session.scalars(
        select(GenresOrm)
    )
    return genres.all()


@router.get('/genres/{genre_id}', summary='Получить жанр по ID', response_model=ResponseGenreWithGames)
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


@router.delete('/genres/{genre_id}', summary='Удалить жанр')
async def delete_genre(session: SessionDep, genre_id: int):
    query = await session.scalar(
        select(GenresOrm)
        .where(GenresOrm.id == genre_id)
    )
    if query is None:
        raise HTTPException(status_code=404, detail='Жанр не найден!')
    session.delete(query)
    await session.commit()
    return {'msg': 'Жанр удален!'}
