from app.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import GamesOrm

class PlatformsOrm(Base):
    __tablename__ = 'platforms'

    id: Mapped[int] = mapped_column(primary_key=True)
    platform_title: Mapped[str]

    games: Mapped[list['GamesOrm']] = relationship(
        back_populates='platform'
    )