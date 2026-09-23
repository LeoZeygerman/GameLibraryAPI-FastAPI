from pydantic import BaseModel, ConfigDict
from app.schemas.game import ResponseGameForPlatform

class ResponsePlatformWithGames(BaseModel):
    id: int
    platform_title: str 
    games: ResponseGameForPlatform

    model_config = ConfigDict(from_attributes=True)

class CreatePlatform(BaseModel):
    platform_title: str

class ResponsePlatform(BaseModel):
    id: int 
    platform_title: str