from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import GamesOrm

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
        pass
    await session.delete(query)
    await session.commit()
    return {'msg': 'Игра удалена!'}