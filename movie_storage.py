import json
import sys


def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data.

    """
    try:
        with open("movies_database.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: The JSON file 'movies_database.json' was not found.")
        exit(1)
    except json.JSONDecodeError:
        print("Error: The JSON file could not be decoded. Please check the file format.")
        sys.exit(1)


def save_movies(dict_object):
    """
    Gets all  movies dictionary as an argument and saves them to the JSON file.
    """
    with open("movies_database.json", "w") as file:
        file.write(json.dumps(dict_object))


def add_movie(title, rating, year):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies.update({title: {"rating": rating, "year": year}})
    save_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    del movies[title]
    save_movies(movies)


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies[title]["rating"] = rating
    save_movies(movies)
