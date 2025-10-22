from database import Base, engine, SessionLocal
from models import Movie, Rating, Tag, Link
from loaders import load_movies_from_file, load_links_from_file, load_ratings_from_file, load_tags_from_file
from pathlib import Path

# Utwórz tabele
Base.metadata.create_all(bind=engine)

session = SessionLocal()

# Ścieżki
BASE_PATH = Path(__file__).resolve().parent / "files"

movies = load_movies_from_file(BASE_PATH / "movies.csv")
links = load_links_from_file(BASE_PATH / "links.csv")
ratings = load_ratings_from_file(BASE_PATH / "ratings.csv")
tags = load_tags_from_file(BASE_PATH / "tags.csv")

for m in movies:
    session.add(Movie(id=m.id, title=m.title, genres=m.genres))
for l in links:
    session.add(Link(movieId=l.movieId, imdbId=l.imdbId, tmdbId=l.tmdbId))
for r in ratings:
    session.add(Rating(userId=r.userId, movieId=r.movieId, rating=r.rating, timestamp=r.timestamp))
for t in tags:
    session.add(Tag(userId=t.userId, movieId=t.movieId, tag=t.tag, timestamp=t.timestamp))

session.commit()
session.close()
