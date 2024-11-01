from pathlib import Path
import os

DATA_DIR = Path(__file__).parent
DEFAULT_PATH = os.path.join(DATA_DIR, 'default.json')


def get_data_path(filename):
    """Function to get full path of any file inside the data directory"""
    return os.path.join(DATA_DIR, filename)
