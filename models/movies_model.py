from pydantic import BaseModel, Field, field_validator
from typing import Optional
import datetime


class BaseMovie(BaseModel):
    name: str
    price: int = Field(gt=0)
    description: str
    imageUrl: str
    location: str
    genreId: int
    published: bool


class Genre(BaseModel):
    name: str


class MovieResponse(BaseMovie):
    id: int
    published: bool
    createdAt: str
    rating: Optional[int] = None
    genre: Genre

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("Некорректный формат даты")
        return value