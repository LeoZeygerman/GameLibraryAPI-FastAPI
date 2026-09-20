from app.models import Base
from sqlalchemy.orm import Mapped, mapped_column

class GameGenre(Base):
    __tablename__ = 'game_genre'

    game_id: Mapped[int]
    genre_id: Mapped[int]