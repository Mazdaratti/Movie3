import csv
import os
import pandas as pd
from storage.istorage import IStorage


class StorageCsv(IStorage):
    """
        CSV-based implementation of the IStorage interface.
        Handles loading and saving movie data to and from a CSV file.
    """

    def __init__(self, filepath: str):
        """
            Initializes the CSV storage with a given file path.

            Args:
                filepath (str): The path to the CSV file.
        """
        self._database = filepath
        if not os.path.exists(self._database):
            self.save_movies({})

    def get_movies(self) -> dict:
        """
            Loads movie data from the CSV file.

            Returns:
                dict: A dictionary containing movie information.

            Raises:
                csv.Error: If there is an error with the CSV format.
        """

        movies = {}
        try:
            with open(self._database, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    movies[row['Title']] = {
                        "Rating": float(row['Rating']),
                        "Year": int(row['Year']),
                        "Poster": row['Poster'],
                        "IMDB Link": row['IMDB Link'],
                        "Notes": row.get("Notes", "")
                    }
            return movies
        except FileNotFoundError:
            print(f"Error: File '{self._database}' not found. Returning empty movie list.")
            return {}
        except csv.Error as e:
            print(f"Error: Issue with CSV format in '{self._database}'. Details: {e}")
            return {}

    def save_movies(self, dict_object: dict):
        """
            Saves movie data to the CSV file.

            Args:
                dict_object (dict): Dictionary of movies to save.

            Raises:
                IOError: If there is an error writing to the file.
        """

        movies_list = [{'Title': title, **details} for title, details in dict_object.items()]
        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(movies_list)
        # Save to CSV
        df.to_csv(self._database, index=False)
