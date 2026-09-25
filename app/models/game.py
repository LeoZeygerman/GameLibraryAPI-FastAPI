from sqlalchemy import ForeignKey
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.platform import PlatformsOrm
    from app.models.genre import GenresOrm

class GamesOrm(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    game_title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    release_year: Mapped[int]

    platform_id: Mapped[int] = mapped_column(ForeignKey('platforms.id', ondelete='SET NULL'), nullable=True)

    platform: Mapped['PlatformsOrm'] = relationship(
        back_populates='games'
    )

    genres: Mapped[list['GenresOrm']] = relationship(
        secondary='game_genre',
        back_populates='games'
    )
