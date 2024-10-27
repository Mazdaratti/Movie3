import os
import csv
import pytest
from storage.storage_csv import StorageCsv


@pytest.fixture
def setup_csv_file(tmp_path):
    """Fixture to set up a temporary CSV file for testing."""
    csv_file = tmp_path / "test_movies.csv"
    storage = StorageCsv(str(csv_file))

    # Create a default CSV file with a test entry
    with open(csv_file, "w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Rating', 'Year', 'Poster', 'IMDB Link', 'Notes'])
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


def test_get_default_file(setup_csv_file):
    """Test loading movies from the default CSV file."""
    storage, csv_file = setup_csv_file
    movies = storage.get_movies()

    expected_movies = {
        "The Matrix": {
            "Rating": 8.7,
            "Year": 1999,
            "Poster": "http://example.com/matrix.jpg",
            "IMDB Link": "http://imdb.com/matrix",
            "Notes": "A sci-fi classic."
        }
    }

    assert movies == expected_movies, "Movies loaded do not match the expected output."


def test_save_movies(setup_csv_file):
    """Test saving movies to the CSV file."""
    storage, csv_file = setup_csv_file
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


def test_save_and_get_movies(setup_csv_file):
    """Test saving movies and retrieving them from the CSV file."""
    storage, csv_file = setup_csv_file
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


def test_invalid_csv_format(setup_csv_file):
    """Test handling of invalid CSV format."""
    storage, csv_file = setup_csv_file

    # Create a malformed CSV file
    with open(csv_file, "w", newline='', encoding="utf-8") as file:
        file.write("Title,Rating,Year,Poster,IMDB Link\n")  # Missing the Notes header

    movies = storage.get_movies()

    assert movies == {}, "Expected an empty dictionary when the CSV format is invalid."
