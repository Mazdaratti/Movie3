import os
import pytest
from storage.storage_json import StorageJson


@pytest.fixture
def setup_json_file(tmp_path):
    json_file = tmp_path / "test_movies.json"
    storage = StorageJson(str(json_file))
    yield storage, json_file
    if os.path.exists(json_file):
        os.remove(json_file)


def test_add_movie_json(setup_json_file):
    """Test adding a movie to JSON storage."""
    storage, json_file = setup_json_file
    movie = {"Inception": {"Rating": 8.8, "Year": 2010, "Notes": "Sci-fi classic"}}
    storage.add_movie(movie)
    movies = storage.get_movies()
    assert "Inception" in movies
    assert movies["Inception"]["Rating"] == 8.8


def test_delete_movie_json(setup_json_file):
    """Test deleting a movie from JSON storage."""
    storage, json_file = setup_json_file
    movie = {"Inception": {"Rating": 8.8, "Year": 2010}}
    storage.add_movie(movie)
    storage.delete_movie("Inception")
    movies = storage.get_movies()
    assert "Inception" not in movies


def test_update_movie_json(setup_json_file):
    storage, json_file = setup_json_file
    movie = {"Inception": {"Rating": 8.8, "Year": 2010}}
    storage.add_movie(movie)
    storage.update_movie("Inception", "Updated notes")
    movies = storage.get_movies()
    assert movies["Inception"]["Notes"] == "Updated notes"


def test_save_movies(setup_json_file):
    storage, json_file = setup_json_file
    movies_to_save = {
        "Inception": {
            "Rating": 8.8,
            "Year": 2010,
            "Poster": "http://example.com/inception.jpg",
            "IMDB Link": "http://imdb.com/inception",
            "Notes": "A mind-bending thriller."
        }
    }

    storage.save_movies(movies_to_save)
    stored_movies = storage.get_movies()
    assert stored_movies == movies_to_save, "Saved movies do not match the expected output."


def test_save_and_get_movies(setup_json_file):
    storage, json_file = setup_json_file
    movies_to_save = {
        "The Matrix": {
            "Rating": 8.7,
            "Year": 1999,
            "Poster": "http://example.com/matrix.jpg",
            "IMDB Link": "http://imdb.com/matrix",
            "Notes": "A sci-fi classic."
        }
    }

    storage.save_movies(movies_to_save)
    retrieved_movies = storage.get_movies()
    assert retrieved_movies == movies_to_save, "Retrieved movies do not match the saved data."


def test_invalid_json_format(setup_json_file):
    storage, json_file = setup_json_file

    # Create a malformed JSON file
    with open(json_file, "w") as f:
        f.write("This is not a valid JSON")

    movies = storage.get_movies()
    assert movies == {}, "Expected an empty dictionary when the JSON format is invalid."
