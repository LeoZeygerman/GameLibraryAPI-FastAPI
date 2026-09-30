from fastapi import APIRouter
from app.database import SessionDep
from app.schemas.genre import *
from app.services.genre import *

router = APIRouter(prefix='/genres', tags=['Жанры'])

@router.post('/genres', summary='Добавить новый жанр', response_model=ResponseGenre)
async def create_genre_router(session: SessionDep, genre: CreateGenre):
    new_genre = await create_genre(session, genre)
    return new_genre


@router.get('/genres', summary='Получить список всех жанров', response_model=list[ResponseGenre])
async def get_all_genres_router(session: SessionDep):
    genres = await get_all_genres(session)
    return genres


@router.get('/genres/{genre_id}', summary='Получить жанр по ID', response_model=ResponseGenreWithGames)
async def get_genre_by_id_router(session: SessionDep, genre_id: int):
    genre = await get_genre_by_id(session, genre_id)
    return genre


@router.delete('/genres/{genre_id}', summary='Удалить жанр')
async def delete_genre_router(session: SessionDep, genre_id: int):
    genre = await delete_genre(session, genre_id)
    return genre
