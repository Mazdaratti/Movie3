import statistics
import difflib
import random


class Analytics:
    """
        Provides analytical tools for a movie database.

        This class includes methods to calculate and display various statistics,
        randomly select a movie, perform fuzzy searches on movie titles, sort movies
        by rating or release year, and filter movies based on user-specified criteria.

        Attributes:
            movies (object): A data source for movie information, typically implementing
                             a 'get_movies()' method to retrieve a dictionary of movies.

        Methods:
            show_statistics(): Displays average, median, highest, and lowest ratings.
            random_movie(): Selects and displays a random movie from the database.
            fuzzy_search(): Performs a fuzzy search on movie titles based on user input.
            sort_movies(sort_key, reverse_order): Sorts movies by a specified key.
            print_movies(sorted_movies): Prints a list of sorted movies.
            sorted_by_rating(): Sorts and displays movies by rating in descending order.
            sorted_by_year(): Sorts and displays movies by release year based on user preference.
            get_valid_input(prompt, category): Prompts user for valid numerical input with validation.
            filtered_movies(): Filters and displays movies based on minimum rating and year range.
    """
    def __init__(self, movies_data):
        """
            Initializes the Analytics instance with a given movie data source.

            Args:
                movies_data (object): A data source object that has a 'get_movies()' method
                                          to retrieve movie data.
        """
        self.movies = movies_data

    def show_statistics(self):
        """
            Displays statistical information about the movie ratings in the database.

            The function retrieves the list of movies, calculates the average and median
            ratings, and identifies the movies with the highest and lowest ratings. It
            prints the average rating (to one decimal place), the median rating, and the
            titles of the movies with the highest and lowest ratings.
        """
        movies = self.movies.get_movies()
        ratings = [float(movie["Rating"]) for movie in movies.values()]

        if not ratings:
            print("No ratings available.")
            return

        average_rating = sum(ratings) / len(movies)
        median_rating = statistics.median(ratings)
        highest_rating = max(ratings)
        lowest_rating = min(ratings)

        best_movies = {title: movie["Rating"] for title, movie in movies.items()
                       if float(movie["Rating"]) == highest_rating}
        worst_movies = {title: movie["Rating"] for title, movie in movies.items()
                        if float(movie["Rating"]) == lowest_rating}

        print(f"\nAverage rating: {average_rating:.1f}")
        print(f"Median rating: {median_rating:.1f}")

        for title in best_movies:
            print(f"Best movie: {title}, Rating: {highest_rating}")
        for title in worst_movies:
            print(f"Worst movie: {title}, Rating: {lowest_rating}")

    def random_movie(self):
        """
        Selects and displays a random movie from the movie database.

        This function:
        - Retrieves movie data from the storage.
        - Randomly selects one movie from the collection.
        - Prints the movie title and its rating.
        """
        movies = self.movies.get_movies()
        if not movies:
            print("No movies available.")
            return

        title, details = random.choice(list(movies.items()))
        print(f"\nYour movie for tonight: {title}, it's rated {details['Rating']}")

    def fuzzy_search(self):
        """
            Prompts the user for a part of a movie name, then searches through a
            dictionary of movies for titles that closely match the input using fuzzy matching.

            The search is case-insensitive and matches parts of the movie titles.
            If matches are found, it prints out the movie titles along with their ratings.
        """
        movies = self.movies.get_movies()
        if not movies:
            print("No movies available.")
            return

        part_of_name = input("Enter part of movie name: ").strip()

        if not part_of_name:
            print("No input provided.")
            return

        search_words = part_of_name.lower().split()
        normalized_dict = {key: key.lower().split() for key in movies.keys()}
        matched_keys = []
        for word in search_words:
            for original_key, words in normalized_dict.items():
                if difflib.get_close_matches(word, words, n=5, cutoff=0.6):
                    matched_keys.append(original_key)
        if not matched_keys:
            print("No matches found.")
        else:
            for key in matched_keys:
                if key in movies:
                    print(f"{key}, {movies[key]['Rating']}")

    def sort_movies(self, sort_key, reverse_order=False):
        """
        Sorts movies based on the provided key and displays the sorted list.

        This function:
        - Retrieves movie data from the storage.
        - Sorts the movies by the specified key (either 'rating' or 'year').
        - Calls the function to print the sorted movies.

        Parameters:
        - sort_key (str): The key to sort movies by ('rating' or 'year').
        - reverse_order (bool): Whether to sort in descending order.
        """
        movies = self.movies.get_movies()
        if not movies:
            print("No movies available.")
            return None

        return sorted(movies.items(), key=lambda x: x[1][sort_key], reverse=reverse_order)

    @staticmethod
    def print_movies(sorted_movies):
        """
        Prints the sorted movies.

        This function:
        - Takes a list of sorted movie items.
        - Displays each movie's title, release year, and rating.

        Parameters:
        - sorted_movies (list): A list of sorted movie tuples (title, details).
        - sort_key (str): The key by which the movies were sorted.
        """
        for title, details in sorted_movies:
            print(f"{title} ({details['Year']}): {details['Rating']}")

    def sorted_by_rating(self):
        """
        Sorts and displays movies by their rating in descending order.
        """
        sorted_movies = self.sort_movies("Rating", True)
        if sorted_movies:
            self.print_movies(sorted_movies)

    def sorted_by_year(self):
        """
        Sorts and displays movies by their release year.

        Prompts the user to choose whether to display the latest movies first.
        """
        prompt = "Do you want the latest movies first? (Y/N) "

        while (user_choice := input(prompt).strip().lower()) not in {"y", "n"}:
            print('Please enter "Y" or "N"')

        sort_descending = user_choice == "y"
        sorted_movies = self.sort_movies("Year", sort_descending)
        if sorted_movies:
            self.print_movies(sorted_movies)

    @staticmethod
    def get_valid_input(prompt, category):
        """
        Prompts the user for a valid numerical input and performs category-based validation.

        Args:
            prompt (str): The message to display when asking for input.
            category (str): The type of value to validate ('year' or 'rating').

        Returns:
            float or None: The validated numerical value, or None if the input is left blank.

        Raises:
            ValueError: If the input is not a valid number or does not meet category-based validation rules.
        """
        while True:
            user_input = input(prompt).strip()
            if not user_input:
                return None
            try:
                value = float(user_input)
                if value < 0 or (category == "Year" and "." in user_input):
                    raise ValueError
                return value
            except ValueError:
                print(f"Please enter a valid {category}.")

    def filtered_movies(self):
        """
        Filters and displays movies based on user-specified criteria for minimum rating, start year, and end year.

        Prompts the user to input a minimum rating, start year, and end year. These inputs are validated as follows:
        - Rating must be a positive float or integer.
        - Year must be a positive integer (no decimals).
        If the user leaves a field blank, that criterion is ignored (no filter applied).

        After filtering, the function displays the movies that match the criteria or a message if no matches are found.

        Output:
            - Prints the filtered list of movies or a message if no matches are found.
        """
        movies = self.movies.get_movies()
        if not movies:
            print("No movies available.")
            return

        start_rating = self.get_valid_input("Enter minimum rating (leave blank for no minimum rating): ", "rating")
        start_year = self.get_valid_input("Enter start year (leave blank for no start year): ", "year")
        end_year = self.get_valid_input("Enter end year (leave blank for no end year): ", "year")

        filtered_movie_list = [(title, details) for title, details in movies.items()
                               if (start_rating is None or float(details["Rating"]) >= start_rating) and
                               (start_year is None or int(details["Year"]) >= start_year) and
                               (end_year is None or int(details["Year"]) <= end_year)
                               ]

        self.print_movies(filtered_movie_list) if filtered_movie_list else print("No movies match for given criteria.")
