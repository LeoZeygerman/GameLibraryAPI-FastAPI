from app.routers.game import router
from app.database import SessionDep
from app.schemas.genre import CreateGenre
from app.models.genre import GenresOrm

@router.post('/new-genre', summary='Добавить новый жанр')
async def create_genre(session: SessionDep, genre: CreateGenre):
    new_genre = GenresOrm(genre_title = genre.genre_title)
    session.add(new_genre)
    await session.commit()
    return f'Жанр {genre.genre_title} добавлен!'
