from fastapi import APIRouter
from app.database import SessionDep
from app.schemas.game import *
from app.services.game import *

router = APIRouter(prefix='/games', tags=['Игры'])

@router.post('/', summary='Добавить игру', response_model=ResponseGame)
async def create_game_router(session: SessionDep, game: CreateGame):
    new_game = await create_game(session, game)
    return new_game


@router.get('/get-by-name/{game_name}', summary='Получить игру по названию', response_model=ResponseGame)
async def get_game_by_name_router(session: SessionDep, game_name: str):
    game = await get_game_by_name(session, game_name)
    return game


@router.patch('/update/{game_name}', summary='Изменить игру', response_model=ResponseGame)
async def update_game_router(session: SessionDep, game_name: str, game_data: UpdateGame):
    game = await update_game(session, game_name, game_data)
    return game


@router.delete('/delete/{game_id}', summary='Удалить игру')
async def delete_game_router(session: SessionDep, game_id: int):
    game = await delete_game_by_id(session, game_id)
    return game
