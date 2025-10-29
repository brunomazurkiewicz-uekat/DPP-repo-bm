from __future__ import annotations
from typing import List, Optional
from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select

from database import SessionLocal, engine
from models import Base, Movie, Link, Rating, Tag

app = FastAPI()
Base.metadata.create_all(bind=engine)


# Dependency do sesji
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class MovieOut(BaseModel):
    id: int
    title: str
    genres: str

    class Config:
        orm_mode = True
        from_attributes = True


class LinkOut(BaseModel):
    movieId: int
    imdbId: Optional[int]
    tmdbId: Optional[int]

    class Config:
        orm_mode = True
        from_attributes = True


class RatingOut(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int

    class Config:
        orm_mode = True
        from_attributes = True


class TagOut(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int

    class Config:
        orm_mode = True
        from_attributes = True


# --- Endpointy ---
@app.get("/")
def read_root():
    return {"hello": "world"}


@app.get("/movies", response_model=List[MovieOut])
def get_movies(limit: int | None = None, db: Session = Depends(get_db)):
    stmt = select(Movie)
    if limit:
        stmt = stmt.limit(limit)
    return list(db.scalars(stmt))


@app.get("/links", response_model=List[LinkOut])
def get_links(limit: int | None = None, db: Session = Depends(get_db)):
    stmt = select(Link)
    if limit:
        stmt = stmt.limit(limit)
    return list(db.scalars(stmt))


@app.get("/ratings", response_model=List[RatingOut])
def get_ratings(
    movieId: int | None = None,
    userId: int | None = None,
    limit: int | None = None,
    db: Session = Depends(get_db),
):
    stmt = select(Rating)
    if movieId:
        stmt = stmt.where(Rating.movieId == movieId)
    if userId:
        stmt = stmt.where(Rating.userId == userId)
    if limit:
        stmt = stmt.limit(limit)
    return list(db.scalars(stmt))


@app.get("/tags", response_model=List[TagOut])
def get_tags(limit: int | None = None, db: Session = Depends(get_db)):
    stmt = select(Tag)
    if limit:
        stmt = stmt.limit(limit)
    return list(db.scalars(stmt))
