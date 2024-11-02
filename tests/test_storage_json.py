import os
import pytest
from storage.storage_json import StorageJson


# Disable Pylint warning for redefined-outer-name specifically for the setup_json_file fixture
# pylint: disable=redefined-outer-name
@pytest.fixture
def setup_json_file(tmp_path):
    """
    Pytest fixture to set up a temporary JSON file for testing.
    Initializes the StorageJson instance and removes the test file after each test.

    Args:
        tmp_path (Path): Temporary directory provided by pytest.

    Yields:
        tuple: StorageJson instance and the path to the test JSON file.
    """
    json_file = tmp_path / "test_movies.json"
    storage = StorageJson(str(json_file))
    yield storage, json_file
    if os.path.exists(json_file):
        os.remove(json_file)


def test_add_movie_json(setup_json_file):
    """
    Test the add_movie method of StorageJson.

    Verifies that the movie is added correctly by checking if:
    - The title is present in the stored movies.
    - The rating matches the added data.
    """
    storage, _ = setup_json_file
    movie = {"Inception": {"Rating": 8.8, "Year": 2010, "Notes": "Sci-fi classic"}}
    storage.add_movie(movie)
    movies = storage.get_movies()
    assert "Inception" in movies
    assert movies["Inception"]["Rating"] == 8.8


def test_delete_movie_json(setup_json_file):
    """
    Test the delete_movie method of StorageJson.

    Verifies that the specified movie is removed by:
    - Adding a movie to the JSON file.
    - Deleting the movie by title.
    - Checking that the title is no longer in stored movies.
    """
    storage, _ = setup_json_file
    movie = {"Inception": {"Rating": 8.8, "Year": 2010}}
    storage.add_movie(movie)
    storage.delete_movie("Inception")
    movies = storage.get_movies()
    assert "Inception" not in movies


def test_update_movie_json(setup_json_file):
    """
    Test the update_movie method of StorageJson.

    Verifies that the specified movie is updated by:
    - Adding a movie to the JSON file.
    - Updating the movie's notes.
    - Checking that the updated notes are saved correctly.
    """
    storage, _ = setup_json_file
    movie = {"Inception": {"Rating": 8.8, "Year": 2010}}
    storage.add_movie(movie)
    storage.update_movie("Inception", "Updated notes")
    movies = storage.get_movies()
    assert movies["Inception"]["Notes"] == "Updated notes"


def test_save_and_get_movies(setup_json_file):
    """
    Test the save_movies and get_movies methods of StorageJson.

    Verifies that movies are saved and retrieved accurately by:
    - Saving a dictionary of movies.
    - Retrieving the movies from storage.
    - Asserting that retrieved data matches saved data.
    """
    storage, _ = setup_json_file
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
    """
    Test handling of invalid JSON format in get_movies.

    Verifies that when the JSON file format is invalid:
    - The method returns an empty dictionary.
    - An error message is displayed.
    """
    storage, json_file = setup_json_file

    # Create a malformed JSON file
    with open(json_file, "w", encoding="utf-8") as f:
        f.write("This is not a valid JSON")

    movies = storage.get_movies()
    assert movies == {}, "Expected an empty dictionary when the JSON format is invalid."
