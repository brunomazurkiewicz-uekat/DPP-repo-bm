from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    genres = Column(Text, nullable=False)


class Link(Base):
    __tablename__ = "links"

    # klucz główny = movieId, poprawne użycie ForeignKey:
    movieId = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    imdbId = Column(Integer, nullable=True)
    tmdbId = Column(Integer, nullable=True)


class Rating(Base):
    __tablename__ = "ratings"

    # przykład złożonego klucza: (userId, movieId, timestamp)
    userId = Column(Integer, primary_key=True)
    movieId = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    rating = Column(Float, nullable=False)
    timestamp = Column(Integer, primary_key=True)


class Tag(Base):
    __tablename__ = "tags"

    # złożony klucz: (userId, movieId, tag, timestamp)
    userId = Column(Integer, primary_key=True)
    movieId = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    tag = Column(String, primary_key=True)
    timestamp = Column(Integer, primary_key=True)
