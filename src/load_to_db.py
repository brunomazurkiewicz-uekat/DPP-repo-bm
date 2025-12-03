# src/load_to_db.py
from .database import SessionLocal, engine, Base
from .models import Movie, Link, Rating, Tag
from .loaders import (
    load_movies_csv,
    load_links_csv,
    load_ratings_csv,
    load_tags_csv,
)


def load_all():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Czyścimy tabele (opcjonalnie)
        db.query(Tag).delete()
        db.query(Rating).delete()
        db.query(Link).delete()
        db.query(Movie).delete()
        db.commit()

        # MOVIES
        for m in load_movies_csv():
            movie = Movie(
                id=m["id"],
                title=m["title"],
                genres=m["genres"],
            )
            db.add(movie)

        # LINKS
        for l in load_links_csv():
            link = Link(
                movieId=l["movieId"],
                imdbId=l["imdbId"],
                tmdbId=l["tmdbId"],
            )
            db.add(link)

        # RATINGS
        for r in load_ratings_csv():
            rating = Rating(
                userId=r["userId"],
                movieId=r["movieId"],
                rating=r["rating"],
                timestamp=r["timestamp"],
            )
            db.add(rating)

        # TAGS
        for t in load_tags_csv():
            tag = Tag(
                userId=t["userId"],
                movieId=t["movieId"],
                tag=t["tag"],
                timestamp=t["timestamp"],
            )
            db.add(tag)

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    load_all()
    print("Dane załadowane do bazy .movies.db")
