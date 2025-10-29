from __future__ import annotations
from pathlib import Path
from typing import List, Optional
import csv

FILES_DIR = Path(__file__).resolve().parent.parent / "files"


def _to_int_or_none(v: str) -> Optional[int]:
    v = (v or "").strip()
    return int(v) if v.isdigit() else None


def load_movies_from_file(path: Path | None = None) -> List[dict]:
    p = path or (FILES_DIR / "movies.csv")
    if not p.exists():
        raise FileNotFoundError(f"No such file or directory: {p}")

    movies = []
    with p.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "title" not in (reader.fieldnames or []):
            f.seek(0)
            raw = csv.reader(f)
            for row in raw:
                if not row or len(row) < 3:
                    continue
                if row[0].strip().lower() in {"movieid", "id"}:
                    continue
                movies.append({"id": int(row[0]), "title": row[1], "genres": row[2]})
            return movies

        for r in reader:
            mid = r.get("movieId") or r.get("id")
            if not mid:
                continue
            movies.append({"id": int(mid), "title": r["title"], "genres": r["genres"]})
        return movies


def load_links_from_file(path: Path | None = None) -> List[dict]:
    p = path or (FILES_DIR / "links.csv")
    if not p.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku: {p}")

    links = []
    with p.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if not r:
                continue
            links.append({
                "movieId": int(r["movieId"]),
                "imdbId": _to_int_or_none(r.get("imdbId", "")),
                "tmdbId": _to_int_or_none(r.get("tmdbId", "")),
            })
    return links


def load_ratings_from_file(path: Path | None = None) -> List[dict]:
    p = path or (FILES_DIR / "ratings.csv")
    if not p.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku: {p}")

    ratings = []
    with p.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if not r:
                continue
            ratings.append({
                "userId": int(r["userId"]),
                "movieId": int(r["movieId"]),
                "rating": float(r["rating"]),
                "timestamp": int(r["timestamp"]),
            })
    return ratings


def load_tags_from_file(path: Path | None = None) -> List[dict]:
    p = path or (FILES_DIR / "tags.csv")
    if not p.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku: {p}")

    tags = []
    with p.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if not r:
                continue
            tags.append({
                "userId": int(r["userId"]),
                "movieId": int(r["movieId"]),
                "tag": r["tag"],
                "timestamp": int(r["timestamp"]),
            })
    return tags