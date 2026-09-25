from pydantic import BaseModel, ConfigDict
from app.schemas.genre import ResponseGenre
from app.schemas.platform import ResponsePlatform
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.genre import ResponseGenre
    from app.schemas.platform import ResponsePlatform

class CreateGame(BaseModel):
    game_title: str
    description: str
    release_year: int
    platform: str
    genres: list[str]

class ResponseGame(BaseModel):
    id: int
    game_title: str
    description: str
    release_year: int
    platform: list[ResponsePlatform]
    genres: list[ResponseGenre]

    model_config = ConfigDict(from_attributes=True)

class UpdateGame(BaseModel):
    game_title: str | None = None
    description: str | None = None
    release_year: int | None = None
    platform: str | None = None
    genres: list[str] | None = None

class ResponseGameForGenre(BaseModel):
    game_title: str
    release_year: int
    platform: ResponsePlatform

    model_config = ConfigDict(from_attributes=True)


class ResponseGameForPlatform(BaseModel):
    game_title: str
    genres: list[ResponseGenre]