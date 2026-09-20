from app.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class GameGenre(Base):
    __tablename__ = 'game_genre'

    id: Mapped[int] = mapped_column(primary_key=True)

    game_id: Mapped[int] = mapped_column(
        ForeignKey = 'games.id',
        ondelete='CASCADE')
    
    genre_id: Mapped[int] = mapped_column(
        ForeignKey = 'genres.id', 
        ondelete='CASCADE')
