from pydantic import BaseModel, ConfigDict
from app.schemas.game import ResponseGameForGenre

class CreateGenre(BaseModel):
    genre_title: str

class ResponseGenre(BaseModel):
    genre_title: str

    model_config = ConfigDict(from_attributes=True)

class ResponseGenreWithGames(BaseModel):
    genre_title: str
    games: list[ResponseGameForGenre]

    model_config = ConfigDict(from_attributes=True)