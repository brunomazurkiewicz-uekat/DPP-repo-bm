from sqlalchemy import Column, Integer, String, Float,  ForeignKey
from database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    genres = Column(String)


class Rating(Base):
    __tablename__ = "ratings"

    userId = Column(Integer, primary_key=True)
    movieId = Column(Integer, ForeignKey="movies.id")
    rating = Column(Float)
    timestamp = Column(Integer)


class Tag(Base):
    __tablename__ = "tags"

    userId = Column(Integer, primary_key=True)
    movieId = Column(Integer, ForeignKey("movies.id"))
    tag = Column(String)
    timestamp = Column(Integer)


class Link(Base):
    __tablename__ = "links"

    movieId = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    imdbId = Column(Integer, nullable=True)
    tmdbId = Column(Integer, nullable=True)
