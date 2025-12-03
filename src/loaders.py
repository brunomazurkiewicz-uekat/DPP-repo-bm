# src/loaders.py
import csv
from pathlib import Path
from typing import List, Dict, Any


BASE_DIR = Path(__file__).resolve().parent.parent
FILES_DIR = BASE_DIR / "files"


def _to_int_or_none(v: str):
    v = (v or "").strip()
    return int(v) if v.isdigit() else None


def load_movies_csv() -> List[Dict[str, Any]]:
    path = FILES_DIR / "movies.csv"
    rows: List[Dict[str, Any]] = []

    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        # jeśli plik nie ma nagłówków, przełączamy się na zwykły reader
        if not reader.fieldnames or "title" not in reader.fieldnames:
            f.seek(0)
            raw_reader = csv.reader(f)
            for row in raw_reader:
                if not row or len(row) < 3:
                    continue
                if row[0].strip().lower() in {"movieid", "id"}:
                    continue
                rows.append(
                    {
                        "id": int(row[0]),
                        "title": row[1],
                        "genres": row[2],
                    }
                )
            return rows

        for r in reader:
            if not r:
                continue
            movie_id = r.get("movieId") or r.get("id")
            if not movie_id:
                continue
            rows.append(
                {
                    "id": int(movie_id),
                    "title": r.get("title", ""),
                    "genres": r.get("genres", ""),
                }
            )

    return rows


def load_links_csv() -> List[Dict[str, Any]]:
    path = FILES_DIR / "links.csv"
    links: List[Dict[str, Any]] = []

    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if not r:
                continue
            links.append(
                {
                    "movieId": int(r["movieId"]),
                    "imdbId": _to_int_or_none(r.get("imdbId", "")),
                    "tmdbId": _to_int_or_none(r.get("tmdbId", "")),
                }
            )
    return links


def load_ratings_csv() -> List[Dict[str, Any]]:
    path = FILES_DIR / "ratings.csv"
    ratings: List[Dict[str, Any]] = []

    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if not r:
                continue
            ratings.append(
                {
                    "userId": int(r["userId"]),
                    "movieId": int(r["movieId"]),
                    "rating": float(r["rating"]),
                    "timestamp": int(r["timestamp"]),
                }
            )
    return ratings


def load_tags_csv() -> List[Dict[str, Any]]:
    path = FILES_DIR / "tags.csv"
    tags: List[Dict[str, Any]] = []

    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if not r:
                continue
            tags.append(
                {
                    "userId": int(r["userId"]),
                    "movieId": int(r["movieId"]),
                    "tag": r["tag"],
                    "timestamp": int(r["timestamp"]),
                }
            )
    return tags
