from pydantic import BaseModel
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
    description: str
    release_year: int
    platform: ResponsePlatform
    genre: ResponseGenre

class ResponseGameForGenre(BaseModel):
    game_title: str
    release_year: int
    platform: str