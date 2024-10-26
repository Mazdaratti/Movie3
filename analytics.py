import statistics
import difflib
import random
from movie_storage import get_movies


def show_statistics():
    """
        Displays statistical information about the movie ratings in the database.

        The function retrieves the list of movies, calculates the average and median
        ratings, and identifies the movies with the highest and lowest ratings. It
        prints the average rating (to one decimal place), the median rating, and the
        titles of the movies with the highest and lowest ratings.
    """
    movies = get_movies()
    ratings = [movie["rating"] for movie in movies.values()]

    if not ratings:
        print("No ratings available.")
        return

    average_rating = sum(ratings) / len(movies)
    median_rating = statistics.median(ratings)
    highest_rating = max(ratings)
    lowest_rating = min(ratings)

    best_movies = {title: movie["rating"] for title, movie in movies.items() if movie["rating"] == highest_rating}
    worst_movies = {title: movie["rating"] for title, movie in movies.items() if movie["rating"] == lowest_rating}

    print(f"\nAverage rating: {average_rating:.1f}")
    print(f"Median rating: {median_rating:.1f}")

    for title in best_movies:
        print(f"Best movie: {title}, Rating: {highest_rating}")
    for title in worst_movies:
        print(f"Worst movie: {title}, Rating: {lowest_rating}")


def random_movie():
    """
    Selects and displays a random movie from the movie database.

    This function:
    - Retrieves movie data from the storage.
    - Randomly selects one movie from the collection.
    - Prints the movie title and its rating.
    """
    movies = get_movies()
    if not movies:
        print("No movies available.")
        return

    title, details = random.choice(list(movies.items()))
    print(f"\nYour movie for tonight: {title}, it's rated {details['rating']}")


def fuzzy_search():
    """
        Prompts the user for a part of a movie name, then searches through a
        dictionary of movies for titles that closely match the input using fuzzy matching.

        The search is case-insensitive and matches parts of the movie titles.
        If matches are found, it prints out the movie titles along with their ratings.
    """
    movies = get_movies()
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
                print(f"{key}, {movies[key]['rating']}")


def sort_movies(sort_key, reverse_order=False):
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
    movies = get_movies()
    if not movies:
        print("No movies available.")
        return None

    return sorted(movies.items(), key=lambda x: x[1][sort_key], reverse=reverse_order)


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
        print(f"{title} ({details['year']}): {details['rating']}")


def sorted_by_rating():
    """
    Sorts and displays movies by their rating in descending order.
    """
    sorted_movies = sort_movies("rating", True)
    if sorted_movies:
        print_movies(sorted_movies)


def sorted_by_year():
    """
    Sorts and displays movies by their release year.

    Prompts the user to choose whether to display the latest movies first.
    """
    prompt = "Do you want the latest movies first? (Y/N) "

    while (user_choice := input(prompt).strip().lower()) not in {"y", "n"}:
        print('Please enter "Y" or "N"')

    sort_descending = user_choice == "y"
    sorted_movies = sort_movies("year", sort_descending)
    if sorted_movies:
        print_movies(sorted_movies)


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
            if value < 0 or (category == "year" and "." in user_input):
                raise ValueError
            return value
        except ValueError:
            print(f"Please enter a valid {category}.")


def filtered_movies():
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
    movies = get_movies()
    if not movies:
        print("No movies available.")
        return

    start_rating = get_valid_input("Enter minimum rating (leave blank for no minimum rating): ", "rating")
    start_year = get_valid_input("Enter start year (leave blank for no start year): ", "year")
    end_year = get_valid_input("Enter end year (leave blank for no end year): ", "year")

    filtered_movie_list = [(title, details) for title, details in movies.items()
                           if (start_rating is None or details["rating"] >= start_rating) and
                              (start_year is None or details["year"] >= start_year) and
                              (end_year is None or details["year"] <= end_year)
                           ]

    print_movies(filtered_movie_list) if filtered_movie_list else print("No movies match for given criteria.")
