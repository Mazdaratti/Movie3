from abc import ABC, abstractmethod


class IStorage(ABC):
    """
        Interface for movie storage operations.
        Defines the methods required for getting, saving, adding, updating,
        and deleting movies from a storage source.
    """

    @abstractmethod
    def get_movies(self):
        """
            Retrieves movies from storage.

            Returns:
                dict: A dictionary containing movie data.
        """

    @abstractmethod
    def save_movies(self, dict_object: dict):
        """
            Saves movies to storage.

            Args:
                dict_object (dict): The dictionary object containing movie data to be saved.
        """

    def add_movie(self, movie: dict):
        """
            Adds a new movie entry to the storage database.

            Args:
                movie (dict): Dictionary containing movie details (title, rating, etc.).
        """
        movies = self.get_movies()
        movies.update(movie)
        self.save_movies(movies)

    def delete_movie(self, title: str):
        """
            Removes a movie entry from storage by its title.

            Args:
                title (str): The title of the movie to be deleted.
        """
        movies = self.get_movies()
        if title in movies:
            del movies[title]
            self.save_movies(movies)

    def update_movie(self, title: str, notes: str):
        """
            Updates the specified movie with additional notes.

            Args:
                title (str): The title of the movie to be updated.
                notes (str): The notes to add to the movie.
        """
        movies = self.get_movies()
        if title in movies:
            movies[title]["Notes"] = notes
            self.save_movies(movies)
