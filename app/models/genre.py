from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game import GamesOrm

class GenresOrm(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(primary_key=True)
    genre_title: Mapped[str] = mapped_column(unique=True)

    games: Mapped[list['GamesOrm']] = relationship(
        secondary='game_genre',
        back_populates='genres'
    )