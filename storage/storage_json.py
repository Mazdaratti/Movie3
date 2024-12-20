import json
import os
from storage.istorage import IStorage


class StorageJson(IStorage):
    """
        JSON-based implementation of the IStorage interface.
        Handles loading and saving movie data to and from a JSON file.
    """

    def __init__(self, filepath: str):
        """
            Initializes the JSON storage with a specified file path.

            Args:
                filepath (str): The path to the JSON file.
        """
        self._database = filepath
        if not os.path.exists(self._database):
            self.save_movies({})

    def get_movies(self) -> dict:
        """
            Loads movie data from the JSON file.

            Returns:
                dict: A dictionary containing movie information.

            Raises:
                JSONDecodeError: If the JSON file format is invalid.
        """

        try:
            with open(self._database, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error: The JSON file could not be decoded. Please check the file format.")
            return {}
        except FileNotFoundError:
            print(f"Error: File '{self._database}' not found. Returning empty movie list.")
            return {}

    def save_movies(self, dict_object: dict):
        """
        Saves the movies dictionary to the JSON file.

        Args:
            dict_object (dict): Dictionary of movies to save.

        Raises:
            IOError: If there is an error writing to the file.
        """
        try:
            with open(self._database, "w", encoding="utf-8") as file:
                json.dump(dict_object, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Error: Unable to write to the file '{self._database}'. Details: {e}")
