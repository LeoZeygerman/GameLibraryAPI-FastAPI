from app.models import Base, GamesOrm
from sqlalchemy.orm import Mapped, mapped_column, relationship

class GenresOrm(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(primary_key=True)
    genre_title: Mapped[str]

    games: Mapped['GamesOrm'] = relationship(
        secondary='game_genre',
        back_populates='genres'
    )