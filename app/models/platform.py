from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game import GamesOrm

class PlatformsOrm(Base):
    __tablename__ = 'platforms'

    id: Mapped[int] = mapped_column(primary_key=True)
    platform_title: Mapped[str] = mapped_column(unique=True)

    games: Mapped[list['GamesOrm']] = relationship(
        back_populates='platform'
    )