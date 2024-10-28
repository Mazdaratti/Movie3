import os
import sys
from pathlib import Path
from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson
from movie_app import MovieApp


ROOT_PATH = Path(__file__).parent


def get_storage_arg():
    """
        Get the storage file path from command line arguments.

        If no arguments are provided, returns the default path
        to the default JSON storage file. If a valid CSV or JSON
        file is provided as an argument, constructs the full path
        to that file. If the provided file has an invalid extension,
        defaults to the JSON storage file.

        Returns:
            str: The full path to the storage file.
    """
    default_path = os.path.join(ROOT_PATH, "data", "default.json")

    if len(sys.argv) <= 1:
        return default_path
    storage = sys.argv[1]
    if storage.endswith(".csv") or storage.endswith(".json"):
        full_path = os.path.join(ROOT_PATH, "data", storage)
    else:
        print("Wrong file input, sets default storage.")
        full_path = default_path
    return full_path


def main():
    """
        Initialize and run the MovieApp.

        This function determines the storage type based on the file
        extension of the provided storage path. It initializes the
        appropriate storage class and the MovieApp, then starts the
        application.
    """
    storage_path = get_storage_arg()
    if storage_path.endswith(".csv"):
        storage = StorageCsv(storage_path)
    else:
        storage = StorageJson(storage_path)
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == '__main__':
    main()

