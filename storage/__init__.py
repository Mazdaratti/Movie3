from pathlib import Path
from .storage_csv import StorageCsv
from .storage_json import StorageJson

STORAGE_LOADERS = {
    '.csv': StorageCsv,
    '.json': StorageJson
}


# Storage loaders mapping for each file type
def init_storage(path):
    """
        Initializes the storage handler based on the file extension.
    """
    return STORAGE_LOADERS.get(Path(path).suffix)(path)


def is_valid_path(storage_path):
    """
        Checks if the provided storage path has a valid file extension.
    """
    return Path(storage_path).suffix in STORAGE_LOADERS
