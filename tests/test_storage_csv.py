import os
import csv
import pytest
from storage.storage_csv import StorageCsv


# Disable Pylint warning for redefined-outer-name specifically for the setup_csv_file fixture
# pylint: disable=redefined-outer-name
@pytest.fixture
def setup_csv_file(tmp_path):
    """
    Pytest fixture to set up a temporary CSV file for testing.
    Initializes the StorageCsv instance and creates a default movie entry
    to be used in the test cases.

    Args:
        tmp_path (Path): Temporary directory provided by pytest.

    Yields:
        tuple: StorageCsv instance and the path to the test CSV file.
    """
    csv_file = tmp_path / "test_movies.csv"
    storage = StorageCsv(str(csv_file))

    # Create a default CSV file with a test entry
    with open(csv_file, "w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            'Title', 'Rating', 'Year', 'Poster', 'IMDB Link', 'Notes'])
        writer.writeheader()
        writer.writerow({
            'Title': 'The Matrix',
            'Rating': 8.7,
            'Year': 1999,
            'Poster': 'http://example.com/matrix.jpg',
            'IMDB Link': 'http://imdb.com/matrix',
            'Notes': 'A sci-fi classic.'
        })

    yield storage, csv_file

    if os.path.exists(csv_file):
        os.remove(csv_file)


def test_add_movie_csv(setup_csv_file):
    """
    Test the add_movie method of StorageCsv.

    Verifies that the movie is correctly added by:
    - Checking if the title is in the stored movies.
    - Asserting the rating matches the expected value.
    """
    storage, _ = setup_csv_file
    movie = {"Inception": {"Year": 2010,
                           "Rating": 8.8,
                           "Poster": "https://m.media-amazon.com/images/example.jpg",
                           "IMDB Link": "https://www.imdb.com/title/tt1375666/",
                           "Notes": "Sci-fi classic"}}
    storage.add_movie(movie)
    movies = storage.get_movies()
    assert "Inception" in movies
    assert movies["Inception"]["Rating"] == 8.8


def test_delete_movie_csv(setup_csv_file):
    """
    Test the delete_movie method of StorageCsv.

    Verifies that the specified movie is removed by:
    - Adding a movie to the CSV file.
    - Deleting the movie by title.
    - Checking that the title is no longer in stored movies.
    """
    storage, _ = setup_csv_file
    movie = {"Inception": {"Year": 2010,
                           "Rating": 8.8,
                           "Poster": "https://m.media-amazon.com/images/example.jpg",
                           "IMDB Link": "https://www.imdb.com/title/tt1375666/",
                           "Notes": "Sci-fi classic"}}
    storage.add_movie(movie)
    storage.delete_movie("Inception")
    movies = storage.get_movies()
    assert "Inception" not in movies


def test_update_movie_csv(setup_csv_file):
    """
    Test the update_movie method of StorageCsv.

    Verifies that the specified movie is updated by:
    - Adding a movie to the CSV file.
    - Updating the movie's notes.
    - Checking that the updated notes are saved correctly.
    """
    storage, _ = setup_csv_file
    movie = {"Inception": {"Year": 2010,
                           "Rating": 8.8,
                           "Poster": "https://m.media-amazon.com/images/example.jpg",
                           "IMDB Link": "https://www.imdb.com/title/tt1375666/",
                           "Notes": "Sci-fi classic"}}
    storage.add_movie(movie)
    storage.update_movie("Inception", "Updated notes")
    movies = storage.get_movies()
    assert movies["Inception"]["Notes"] == "Updated notes"


def test_save_and_get_movies(setup_csv_file):
    """
    Test the save_movies and get_movies methods of StorageCsv.

    Verifies that movies are saved and retrieved accurately by:
    - Saving a dictionary of movies.
    - Retrieving the movies from storage.
    - Asserting that retrieved data matches saved data.
    """
    storage, _ = setup_csv_file
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


def test_invalid_csv_format(setup_csv_file):
    """
    Test handling of invalid CSV format in get_movies.

    Verifies that when the CSV file format is invalid:
    - The method returns an empty dictionary.
    - An error message is displayed.
    """
    storage, csv_file = setup_csv_file

    # Create a malformed CSV file
    with open(csv_file, "w", newline='', encoding="utf-8") as file:
        file.write("Title,Rating,Year,Poster,IMDB Link\n")  # Missing the Notes header

    movies = storage.get_movies()

    assert movies == {}, "Expected an empty dictionary when the CSV format is invalid."
