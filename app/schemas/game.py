from pydantic import BaseModel, ConfigDict
from app.schemas.genre import ResponseGenre
from app.schemas.platform import ResponsePlatform

class CreateGame(BaseModel):
    game_title: str
    description: str
    release_year: int
    platform: str
    genre: list[str]

class ResponseGame(BaseModel):
    id: int
    game_title: str
    description: str
    release_year: int
    platform: ResponsePlatform
    genres: ResponseGenre

    model_config = ConfigDict(from_attributes=True)

class ResponseGameForGenre(BaseModel):
    game_title: str
    release_year: int
    platform: ResponsePlatform

    model_config = ConfigDict(from_attributes=True)