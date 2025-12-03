# src/main.py
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from .models import Movie, Link, Rating, Tag

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movies API")


# ---------- DB dependency ----------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Pydantic schematy ----------

# MOVIES
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


# LINKS
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
    id: int

    class Config:
        orm_mode = True


# RATINGS
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
    id: int

    class Config:
        orm_mode = True


# TAGS
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
    id: int

    class Config:
        orm_mode = True


# =========================================================
#                       MOVIES
# =========================================================

@app.get("/movies", response_model=List[MovieOut])
def list_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()


@app.post("/movies", response_model=MovieOut, status_code=status.HTTP_201_CREATED)
def create_movie(data: MovieCreate, db: Session = Depends(get_db)):
    movie = Movie(title=data.title, genres=data.genres)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


@app.get("/movies/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.put("/movies/{movie_id}", response_model=MovieOut)
def update_movie(movie_id: int, data: MovieUpdate, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    if data.title is not None:
        movie.title = data.title
    if data.genres is not None:
        movie.genres = data.genres

    db.commit()
    db.refresh(movie)
    return movie


@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return None


# =========================================================
#                        LINKS
# =========================================================

@app.get("/links", response_model=List[LinkOut])
def list_links(db: Session = Depends(get_db)):
    return db.query(Link).all()


@app.post("/links", response_model=LinkOut, status_code=status.HTTP_201_CREATED)
def create_link(data: LinkCreate, db: Session = Depends(get_db)):
    link = Link(
        movieId=data.movieId,
        imdbId=data.imdbId,
        tmdbId=data.tmdbId,
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@app.get("/links/{link_id}", response_model=LinkOut)
def get_link(link_id: int, db: Session = Depends(get_db)):
    link = db.get(Link, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@app.put("/links/{link_id}", response_model=LinkOut)
def update_link(link_id: int, data: LinkUpdate, db: Session = Depends(get_db)):
    link = db.get(Link, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    if data.imdbId is not None:
        link.imdbId = data.imdbId
    if data.tmdbId is not None:
        link.tmdbId = data.tmdbId

    db.commit()
    db.refresh(link)
    return link


@app.delete("/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(link_id: int, db: Session = Depends(get_db)):
    link = db.get(Link, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    db.delete(link)
    db.commit()
    return None


# =========================================================
#                       RATINGS
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


@app.get("/ratings/{rating_id}", response_model=RatingOut)
def get_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.get(Rating, rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating


@app.put("/ratings/{rating_id}", response_model=RatingOut)
def update_rating(rating_id: int, data: RatingUpdate, db: Session = Depends(get_db)):
    rating = db.get(Rating, rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    if data.rating is not None:
        rating.rating = data.rating
    if data.timestamp is not None:
        rating.timestamp = data.timestamp

    db.commit()
    db.refresh(rating)
    return rating


@app.delete("/ratings/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.get(Rating, rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    db.delete(rating)
    db.commit()
    return None


# =========================================================
#                        TAGS
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


@app.get("/tags/{tag_id}", response_model=TagOut)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@app.put("/tags/{tag_id}", response_model=TagOut)
def update_tag(tag_id: int, data: TagUpdate, db: Session = Depends(get_db)):
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    if data.tag is not None:
        tag.tag = data.tag
    if data.timestamp is not None:
        tag.timestamp = data.timestamp

    db.commit()
    db.refresh(tag)
    return tag


@app.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(tag)
    db.commit()
    return None


# Root dla sanity-check
@app.get("/")
def read_root():
    return {"status": "ok"}
