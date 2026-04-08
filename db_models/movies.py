from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from typing import Dict, Any

Base = declarative_base()

class MoviesDBModel(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime)
    location = Column(String)
    published = Column(Boolean)
    rating = Column(Float)
    genre_id = Column(String)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'image_url': self.image_url,
            'created_at': self.created_at,
            'location': self.location,
            'published': self.published,
            'rating': self.rating,
            'genre_id': self.genre_id
        }

    def __repr__(self):
        return f"<User(id='{self.id}', name='{self.name}')>"