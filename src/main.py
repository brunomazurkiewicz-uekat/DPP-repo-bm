import csv
from pathlib import Path
from typing import Union, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Movie(BaseModel):
    id: int
    title: str
    genres: str


class Rating(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int


class Tag(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int


class Link(BaseModel):
    movieId: int
    imdbId: Optional[int]
    tmdbId: Optional[int]


# --- ŚCIEŻKI DO PLIKÓW ---
RATINGS_PATH = (Path(__file__).resolve().parent.parent / "files" / "ratings.csv")
TAGS_PATH = (Path(__file__).resolve().parent.parent / "files" / "tags.csv")
LINKS_PATH = (Path(__file__).resolve().parent.parent / "files" / "links.csv")
DATA_PATH = (Path(__file__).resolve().parent.parent / "files" / "movies.csv")


# --- LOADERY ---
def load_ratings_from_file(path: Path) -> List[Rating]:
    if not path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku: {path}")
    out: List[Rating] = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row:
                continue
            out.append(
                Rating(
                    userId=int(row["userId"]),
                    movieId=int(row["movieId"]),
                    rating=float(row["rating"]),
                    timestamp=int(row["timestamp"]),
                )
            )
    return out


def load_tags_from_file(path: Path) -> List[Tag]:
    if not path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku: {path}")
    out: List[Tag] = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row:
                continue
            out.append(
                Tag(
                    userId=int(row["userId"]),
                    movieId=int(row["movieId"]),
                    tag=row["tag"],
                    timestamp=int(row["timestamp"]),
                )
            )
    return out


def _to_int_or_none(v: str) -> Optional[int]:
    v = (v or "").strip()
    return int(v) if v.isdigit() else None


def load_links_from_file(path: Path) -> List[Link]:
    if not path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku: {path}")
    out: List[Link] = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row:
                continue
            out.append(
                Link(
                    movieId=int(row["movieId"]),
                    imdbId=_to_int_or_none(row.get("imdbId", "")),
                    tmdbId=_to_int_or_none(row.get("tmdbId", "")),
                )
            )
    return out


def load_movies_from_file(path: Path) -> List[Movie]:
    movies: List[Movie] = []
    if not path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku: {path}")

    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        header_like = set((reader.fieldnames or []))
        if not header_like or len(header_like) < 3 or "title" not in header_like:
            f.seek(0)
            raw_reader = csv.reader(f)
            for row in raw_reader:
                if not row or len(row) < 3:
                    continue
                # Pomijaj ewentualną linię z napisem 'movieId'
                if row[0].strip().lower() in {"movieid", "id"}:
                    continue
                movies.append(
                    Movie(
                        id=int(row[0]),
                        title=row[1],
                        genres=row[2],
                    )
                )
            return movies

        for row in reader:
            if not row:
                continue
            id_field = row.get("id") or row.get("movieId") or row.get("movie_id")
            title = row.get("title") or ""
            genres = row.get("genres") or ""
            if not id_field:
                continue
            movies.append(Movie(id=int(id_field), title=title, genres=genres))

    return movies


# --- ENDPOINTY ---
@app.get("/ratings", response_model=List[Rating])
def get_ratings(limit: int | None = None):
    data = load_ratings_from_file(RATINGS_PATH)
    return data[:limit] if limit else data


@app.get("/tags", response_model=List[Tag])
def get_tags(limit: int | None = None):
    data = load_tags_from_file(TAGS_PATH)
    return data[:limit] if limit else data


@app.get("/links", response_model=List[Link])
def get_links(limit: int | None = None):
    data = load_links_from_file(LINKS_PATH)
    return data[:limit] if limit else data


@app.get("/movies", response_model=List[Movie])
def get_movies():
    return load_movies_from_file(DATA_PATH)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
