import os
import sys
from pathlib import Path
from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson
from movie_app import MovieApp


ROOT_PATH = Path(__file__).parent


def get_storage_arg():
    """Get storage args from terminal call"""
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
    """Main function initialization"""
    storage_path = get_storage_arg()
    if storage_path.endswith(".csv"):
        storage = StorageCsv(storage_path)
    else:
        storage = StorageJson(storage_path)
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == '__main__':
    main()

