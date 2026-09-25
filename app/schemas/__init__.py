from app.schemas.game import ResponseGameForPlatform, ResponseGameForGenre, ResponseGame
from app.schemas.genre import ResponseGenre, ResponseGenreWithGames
from app.schemas.platform import ResponsePlatformWithGames, ResponsePlatform

ResponseGame.model_rebuild()
ResponseGameForGenre.model_rebuild()
ResponseGameForPlatform.model_rebuild()
ResponseGenre.model_rebuild()
ResponseGenreWithGames.model_rebuild()
ResponsePlatformWithGames.model_rebuild()
ResponsePlatform.model_rebuild()