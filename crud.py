import movie_storage


def list_movies():
    """
        Lists all movies in the movie storage with their release years and ratings.

        This function retrieves the list of movies and prints the total count along with
        each movie's title, release year, and rating.
    """
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies available.")
        return

    print(f"\n{len(movies)} movies in total")
    for name, details in movies.items():
        print(f"{name} ({details['year']}): {details['rating']} ")


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
            if user_input_float < 0 or (category == "year" and "." in user_input):
                raise ValueError
            else:
                return user_input_float
        except ValueError:
            print(f"Please enter a valid {category}")


def is_movie_in_dict(name, movies):
    """
        Check if a movie title exists in the dictionary in a case-insensitive manner.

        Args:
            name (str): The movie title to check.
            movies (dict): The dictionary of movies, where keys are movie titles.

        Returns:
            bool: True if the movie title exists in the dictionary (case-insensitive), False otherwise.
    """
    return name.lower() in map(lambda key: key.lower(), movies.keys())


def get_new_title(existing_titles):
    """
        Prompts the user to input a new movie title and ensures it's valid.

        Args:
            existing_titles (dict): A dictionary of existing movies with titles as keys.

        Returns:
            str | None: The new movie name if valid, or None if it already exists.
        """
    while True:
        new_title = input("Enter new movie name: ").strip()
        if not new_title:
            print("Movie name must not be empty.")
        elif is_movie_in_dict(new_title, existing_titles):
            print(f"Movie '{new_title}' already exists!")
            return
        else:
            return new_title


def add_movie():
    """
      Facilitates the addition of a new movie to the movie storage.

      - Prompts the user to enter a new movie name.
      - If the name is valid and does not exist, prompts for a year and rating.
      - Adds the movie to the movie storage.

      Returns:
          None: Exits early if the movie already exists.
      """
    movies = movie_storage.get_movies()
    new_name = get_new_title(movies)
    if not new_name:
        return

    new_year = int(get_num("Enter new movie year: ", "year"))
    new_rating = get_num("Enter new movie rating: ", "rating")

    movie_storage.add_movie(new_name, new_rating, new_year)
    print(f"Movie {new_name} successfully added")


def delete_movie():
    """
       Deletes a movie from the movie storage.

       This function:
       - Prompts the user to enter the name of a movie to delete.
       - Checks if the movie exists in the movie storage.
       - If the movie is found, deletes it from the storage.
       - If the movie is not found, informs the user that the movie doesn't exist.

    """
    movies = movie_storage.get_movies()
    if movies:
        name = input("Enter movie name to delete: ").strip()

        if name in movies:
            movie_storage.delete_movie(name)
            print(f"Movie {name} successfully deleted")
        else:
            print(f"Movie {name} doesn't exist!")
    else:
        print("No movies in database")


def update_movie():
    """
        Updates the rating of an existing movie in the movie storage.

        This function:
        - Prompts the user to enter the name of the movie to update.
        - Checks if the movie exists in the movie storage.
        - If the movie exists, prompts for a new rating and updates the movie.
        - If the movie does not exist, informs the user.
    """
    movies = movie_storage.get_movies()
    if movies:
        name = input("Enter movie name: ").strip()

        if name in movies:
            new_rating = get_num("Enter new movie rating: ", "rating")
            movie_storage.update_movie(name, new_rating)
            print(f"Movie {name} successfully updated")
        else:
            print(f"Movie {name} doesn't exist!")
    else:
        print("No movies in database")
