from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import PlatformsOrm, GenresOrm

class GamesOrm(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    game_title: Mapped[str]
    description: Mapped[str]
    release_year: Mapped[int]

    platform_id: Mapped[int] = mapped_column(ForeignKey('platforms.id'))

    platform: Mapped['PlatformsOrm'] = relationship(
        back_populates='games'
    )

    genres: Mapped[list['GenresOrm']] = relationship(
        secondary='game_genre',
        back_populates='games'
    )
