from pydantic import BaseModel
from app.schemas.game import ResponseGameForGenre

class ResponseGenre(BaseModel):
    genre_title: list[str]

class ResponseGenreWithGames(BaseModel):
    genre_title: str
    games: list[ResponseGameForGenre]