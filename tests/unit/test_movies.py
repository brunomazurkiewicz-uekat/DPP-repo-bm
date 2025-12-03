# tests/unit/test_movies.py
from http import HTTPStatus

from src.models import Movie


def create_sample_movies(db_session):
    movies = [
        Movie(title="Toy Story (1995)", genres="Adventure|Animation|Children|Comedy|Fantasy"),
        Movie(title="Heat (1995)", genres="Action|Crime|Thriller"),
        Movie(title="Jumanji (1995)", genres="Adventure|Children|Fantasy"),
    ]
    db_session.add_all(movies)
    db_session.commit()
    return movies


def test_get_movies_list_returns_all(client, db_session):
    sample_movies = create_sample_movies(db_session)

    resp = client.get("/movies")
    assert resp.status_code == HTTPStatus.OK

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == len(sample_movies)

    titles = {m["title"] for m in data}
    assert "Toy Story (1995)" in titles
    assert "Heat (1995)" in titles
    assert "Jumanji (1995)" in titles


def test_get_movie_by_id_returns_item(client, db_session):
    sample_movies = create_sample_movies(db_session)
    movie = sample_movies[0]

    resp = client.get(f"/movies/{movie.id}")
    assert resp.status_code == HTTPStatus.OK

    data = resp.json()
    assert data["id"] == movie.id
    assert data["title"] == movie.title
    assert data["genres"] == movie.genres


def test_get_movie_by_id_not_found_returns_404(client):
    resp = client.get("/movies/999999")
    assert resp.status_code == HTTPStatus.NOT_FOUND

    body = resp.json()
    assert "not found" in body["detail"].lower()


def test_create_movie_adds_new_record(client):
    payload = {
        "title": "New Movie",
        "genres": "Drama|Romance",
    }

    resp = client.post("/movies", json=payload)
    assert resp.status_code == HTTPStatus.CREATED

    data = resp.json()
    assert "id" in data
    assert data["title"] == payload["title"]
    assert data["genres"] == payload["genres"]

    movie_id = data["id"]

    check_resp = client.get(f"/movies/{movie_id}")
    assert check_resp.status_code == HTTPStatus.OK
    check_data = check_resp.json()
    assert check_data["title"] == payload["title"]


def test_update_movie_changes_data(client, db_session):
    sample_movies = create_sample_movies(db_session)
    movie = sample_movies[1]
    movie_id = movie.id

    update_payload = {
        "title": "Heat (DIRECTOR'S CUT)",
        "genres": "Action|Crime|Thriller",
    }

    resp = client.put(f"/movies/{movie_id}", json=update_payload)
    assert resp.status_code == HTTPStatus.OK

    data = resp.json()
    assert data["id"] == movie_id
    assert data["title"] == update_payload["title"]
    assert data["genres"] == update_payload["genres"]

    check_resp = client.get(f"/movies/{movie_id}")
    check_data = check_resp.json()
    assert check_data["title"] == update_payload["title"]


def test_delete_movie_removes_record(client, db_session):
    sample_movies = create_sample_movies(db_session)
    movie = sample_movies[0]
    movie_id = movie.id

    del_resp = client.delete(f"/movies/{movie_id}")
    assert del_resp.status_code == HTTPStatus.NO_CONTENT

    get_resp = client.get(f"/movies/{movie_id}")
    assert get_resp.status_code == HTTPStatus.NOT_FOUND
