from commands.downloader import MovieInfoDownloader


class Crud:
    def __init__(self, movies_data):
        self.movies = movies_data

    def list_movies(self):
        """
            Lists all movies in the movie storage with their release years and ratings.

            This function retrieves the list of movies and prints the total count along with
            each movie's title, release year, and rating.
        """
        movies = self.movies.get_movies()
        if not movies:
            print("No movies available.")
            return

        print(f"\n{len(movies)} movies in total")
        for name, details in movies.items():
            print(f"{name} ({details['Year']}): {details['Rating']} ")

    @staticmethod
    def get_num(prompt, category):
        """
            Prompts the user to input a numerical value and validates it.

            Args:
                prompt (str): The message to display when asking for input.
                category (str): The type of value to validate (e.g., "year", "rating").

            Returns:
                float: The validated numerical value.

            Raises:
                ValueError: If the input cannot be converted to a float.

            Additional Validation:
                - For "year", ensures the value is positive and has no decimals.
                - For "rating", ensures the value is positive.
        """
        while True:
            user_input = input(prompt)
            try:
                user_input_float = float(user_input)
                if user_input_float < 0 or (category == "Year" and "." in user_input):
                    raise ValueError
                else:
                    return user_input_float
            except ValueError:
                print(f"Please enter a valid {category}")

    def is_movie_in_dict(self, name):
        """
            Check if a movie title exists in the dictionary in a case-insensitive manner.

            Args:
                name (str): The movie title to check.

            Returns:
                bool: True if the movie title exists in the dictionary (case-insensitive), False otherwise.
        """
        movies = self.movies.get_movies()
        return name.lower() in map(lambda key: key.lower(), movies.keys())

    def get_new_title(self):
        """
            Prompts the user to input a new movie title and ensures it's valid.

            Returns:
                str | None: The new movie name if valid, or None if it already exists.
            """
        while True:
            new_title = input("Enter new movie name: ").strip()
            if not new_title:
                print("Movie name must not be empty.")
            elif self.is_movie_in_dict(new_title):
                print(f"Movie '{new_title}' already exists!")
                return
            else:
                return new_title

    def add_movie(self):
        """
          Facilitates the addition of a new movie to the movie storage.

          - Prompts the user to enter a new movie name.
          - If the name is valid and does not exist, prompts for a year and rating.
          - Adds the movie to the movie storage.

          Returns:
              None: Exits early if the movie already exists.
          """
        movies = self.movies.get_movies()
        new_name = self.get_new_title()
        if not new_name:
            return

        new_movie = MovieInfoDownloader().fetch_movie_data(new_name)
        self.movies.add_movie(new_movie)
        print(f"Movie {new_name} successfully added")

    def delete_movie(self):
        """
           Deletes a movie from the movie storage.

           This function:
           - Prompts the user to enter the name of a movie to delete.
           - Checks if the movie exists in the movie storage.
           - If the movie is found, deletes it from the storage.
           - If the movie is not found, informs the user that the movie doesn't exist.

        """
        movies = self.movies.get_movies()
        if movies:
            name = input("Enter movie name to delete: ").strip()

            if name in movies:
                self.movies.delete_movie(name)
                print(f"Movie {name} successfully deleted")
            else:
                print(f"Movie {name} doesn't exist!")
        else:
            print("No movies in database")

    def update_movie(self):
        """
            Updates a movie entry with a personal note.

            This function:
            - Prompts the user to enter the name of the movie to update.
            - Checks if the movie exists in the movie storage.
            - If the movie exists, prompts for a note and updates the movie.
            - If the movie does not exist, informs the user.
        """
        movies = self.movies.get_movies()
        if movies:
            name = input("Enter movie name: ").strip()

            if name in movies:
                note = input("Enter a note to add to the movie: ")
                self.movies.update_movie(name, note)
                print(f"Movie {name} successfully updated")
            else:
                print(f"Movie {name} doesn't exist!")
        else:
            print("No movies in database")
