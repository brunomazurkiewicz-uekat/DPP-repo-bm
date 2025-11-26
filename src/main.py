from __future__ import annotations
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from starlette import status

from src.database import SessionLocal, engine
from src.models import Base, Movie, Link, Rating, Tag



app = FastAPI()
Base.metadata.create_all(bind=engine)


# Dependency do sesji
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Pydantic SCHEMATY ----------

# --- MOVIES ---

class MovieBase(BaseModel):
    title: str
    genres: str


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    genres: Optional[str] = None


class MovieOut(MovieBase):
    id: int

    class Config:
        orm_mode = True


# --- LINKS ---
class LinkBase(BaseModel):
    movieId: int
    imdbId: Optional[int] = None
    tmdbId: Optional[int] = None

class LinkCreate(LinkBase):
    pass


class LinkUpdate(BaseModel):
    imdbId: Optional[int] = None
    tmdbId: Optional[int] = None


class LinkOut(LinkBase):
    class Config:
        orm_mode = True


# --- RATINGS ---

class RatingBase(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int


class RatingCreate(RatingBase):
    pass


class RatingUpdate(BaseModel):
    rating: Optional[float] = None
    timestamp: Optional[int] = None


class RatingOut(RatingBase):
    class Config:
        orm_mode = True


# --- TAGS ---

class TagBase(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    tag: Optional[str] = None
    timestamp: Optional[int] = None


class TagOut(TagBase):
    class Config:
        orm_mode = True

# =========================================================
#                    LINKS – LIST + CRUD
# =========================================================

@app.get("/links", response_model=List[LinkOut])
def list_links(db: Session = Depends(get_db)):
    return db.query(Link).all()


@app.post("/links", response_model=LinkOut, status_code=status.HTTP_201_CREATED)
def create_link(data: LinkCreate, db: Session = Depends(get_db)):
    existing = db.get(Link, data.movieId)
    if existing:
        raise HTTPException(status_code=400, detail="Link for this movie already exists")

    link = Link(
        movieId=data.movieId,
        imdbId=data.imdbId,
        tmdbId=data.tmdbId,
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@app.get("/links/{movie_id}", response_model=LinkOut)
def get_link(movie_id: int, db: Session = Depends(get_db)):
    link = db.get(Link, movie_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@app.put("/links/{movie_id}", response_model=LinkOut)
def update_link(movie_id: int, data: LinkUpdate, db: Session = Depends(get_db)):
    link = db.get(Link, movie_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    if data.imdbId is not None:
        link.imdbId = data.imdbId
    if data.tmdbId is not None:
        link.tmdbId = data.tmdbId

    db.commit()
    db.refresh(link)
    return link


@app.delete("/links/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(movie_id: int, db: Session = Depends(get_db)):
    link = db.get(Link, movie_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    db.delete(link)
    db.commit()
    return None


# =========================================================
#                   RATINGS – LIST + CRUD
#   (klucz złożony: userId + movieId + timestamp)
# =========================================================

@app.get("/ratings", response_model=List[RatingOut])
def list_ratings(db: Session = Depends(get_db)):
    return db.query(Rating).all()


@app.post("/ratings", response_model=RatingOut, status_code=status.HTTP_201_CREATED)
def create_rating(data: RatingCreate, db: Session = Depends(get_db)):
    rating = Rating(
        userId=data.userId,
        movieId=data.movieId,
        rating=data.rating,
        timestamp=data.timestamp,
    )
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating


@app.get(
    "/ratings/{user_id}/{movie_id}/{timestamp}",
    response_model=RatingOut,
)
def get_rating(
    user_id: int,
    movie_id: int,
    timestamp: int,
    db: Session = Depends(get_db),
):
    rating = (
        db.query(Rating)
        .filter(
            Rating.userId == user_id,
            Rating.movieId == movie_id,
            Rating.timestamp == timestamp,
        )
        .first()
    )
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating


@app.put(
    "/ratings/{user_id}/{movie_id}/{timestamp}",
    response_model=RatingOut,
)
def update_rating(
    user_id: int,
    movie_id: int,
    timestamp: int,
    data: RatingUpdate,
    db: Session = Depends(get_db),
):
    rating = (
        db.query(Rating)
        .filter(
            Rating.userId == user_id,
            Rating.movieId == movie_id,
            Rating.timestamp == timestamp,
        )
        .first()
    )
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    if data.rating is not None:
        rating.rating = data.rating
    if data.timestamp is not None:
        rating.timestamp = data.timestamp

    db.commit()
    db.refresh(rating)
    return rating


@app.delete(
    "/ratings/{user_id}/{movie_id}/{timestamp}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_rating(
    user_id: int,
    movie_id: int,
    timestamp: int,
    db: Session = Depends(get_db),
):
    rating = (
        db.query(Rating)
        .filter(
            Rating.userId == user_id,
            Rating.movieId == movie_id,
            Rating.timestamp == timestamp,
        )
        .first()
    )
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    db.delete(rating)
    db.commit()
    return None

# =========================================================
#                     TAGS – LIST + CRUD
#   (klucz złożony: userId + movieId + tag + timestamp)
# =========================================================

@app.get("/tags", response_model=List[TagOut])
def list_tags(db: Session = Depends(get_db)):
    return db.query(Tag).all()


@app.post("/tags", response_model=TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(data: TagCreate, db: Session = Depends(get_db)):
    tag = Tag(
        userId=data.userId,
        movieId=data.movieId,
        tag=data.tag,
        timestamp=data.timestamp,
    )
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@app.get(
    "/tags/{user_id}/{movie_id}/{timestamp}",
    response_model=TagOut,
)
def get_tag(
    user_id: int,
    movie_id: int,
    timestamp: int,
    db: Session = Depends(get_db),
):
    tag = (
        db.query(Tag)
        .filter(
            Tag.userId == user_id,
            Tag.movieId == movie_id,
            Tag.timestamp == timestamp,
        )
        .first()
    )
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@app.put(
    "/tags/{user_id}/{movie_id}/{timestamp}",
    response_model=TagOut,
)
def update_tag(
    user_id: int,
    movie_id: int,
    timestamp: int,
    data: TagUpdate,
    db: Session = Depends(get_db),
):
    tag = (
        db.query(Tag)
        .filter(
            Tag.userId == user_id,
            Tag.movieId == movie_id,
            Tag.timestamp == timestamp,
        )
        .first()
    )
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    if data.tag is not None:
        tag.tag = data.tag
    if data.timestamp is not None:
        tag.timestamp = data.timestamp

    db.commit()
    db.refresh(tag)
    return tag


@app.delete(
    "/tags/{user_id}/{movie_id}/{timestamp}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_tag(
    user_id: int,
    movie_id: int,
    timestamp: int,
    db: Session = Depends(get_db),
):
    tag = (
        db.query(Tag)
        .filter(
            Tag.userId == user_id,
            Tag.movieId == movie_id,
            Tag.timestamp == timestamp,
        )
        .first()
    )
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(tag)
    db.commit()
    return None

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
