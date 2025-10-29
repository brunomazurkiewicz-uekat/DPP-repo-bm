from database import SessionLocal, engine, Base
from models import Movie, Link, Rating, Tag
from loaders import (
    load_movies_from_file,
    load_links_from_file,
    load_ratings_from_file,
    load_tags_from_file,
)

Base.metadata.create_all(bind=engine)
session = SessionLocal()

# Wczytaj dane z CSV
movies = load_movies_from_file()
links = load_links_from_file()
ratings = load_ratings_from_file()
tags = load_tags_from_file()

# Załaduj do bazy
for m in movies:
    session.add(Movie(**m))
for l in links:
    session.add(Link(**l))
for r in ratings:
    session.add(Rating(**r))
for t in tags:
    session.add(Tag(**t))

session.commit()
session.close()

print("Dane załadowane do bazy SQLite (movies.db)")
