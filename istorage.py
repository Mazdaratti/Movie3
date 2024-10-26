from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    Interface for movie storage operations. This abstract base class
    defines the methods required for getting, saving, adding, updating,
    and deleting movies from a storage source.
    """

    @abstractmethod
    def get_movies(self):
        """
        Abstract method to retrieve movies from storage.

        Returns:
            dict: A dictionary containing movie data.
        """
        pass

    @abstractmethod
    def save_movies(self, dict_object: dict):
        """
        Abstract method to save movies to storage.

        Args:
            dict_object (dict): The dictionary object containing movie data to be saved.
        """
        pass

    def add_movie(self, title: str, rating: float, year: int, poster: str, imdb_link: str):
        """
        Adds a movie to the storage database. Loads existing data,
        appends the new movie, and saves it back to storage.

        Args:
            title (str): The movie title.
            rating (float): The movie's rating.
            year (int): The release year of the movie.
            poster (str): URL link to the movie's poster.
            imdb_link (str): IMDB URL link for the movie.
        """
        movies = self.get_movies()
        movies[title] = {
            "Rating": rating,
            "Year": year,
            "Poster": poster,
            "IMDB Link": imdb_link
        }
        self.save_movies(movies)

    def delete_movie(self, title: str):
        """
        Deletes a movie from the storage database by title.

        Args:
            title (str): The title of the movie to be deleted.
        """
        movies = self.get_movies()
        if title in movies:
            del movies[title]
            self.save_movies(movies)

    def update_movie(self, title: str, notes: str):
        """
        Updates the specified movie with new notes.

        Args:
            title (str): The title of the movie to be updated.
            notes (str): The notes to add to the movie.
        """
        movies = self.get_movies()
        if title in movies:
            movies[title]["Notes"] = notes
            self.save_movies(movies)
            