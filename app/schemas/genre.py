from pydantic import BaseModel

class ResponseGenre(BaseModel):
    genre_title: list[str]