# src/models.py
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from .database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    genres = Column(Text, nullable=False)


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    movieId = Column(Integer, nullable=False)  # można dać ForeignKey("movies.id")
    imdbId = Column(Integer, nullable=True)
    tmdbId = Column(Integer, nullable=True)


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, nullable=False)
    movieId = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    timestamp = Column(Integer, nullable=False)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, nullable=False)
    movieId = Column(Integer, nullable=False)
    tag = Column(Text, nullable=False)
    timestamp = Column(Integer, nullable=False)
