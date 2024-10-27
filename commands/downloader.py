import requests
from dotenv import load_dotenv
import os
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


def load_api_key() -> str:
    """
    Load the API key from environment variables.

    Returns:
        str: The loaded API key.

    Raises:
        ValueError: If the API key is missing or invalid.
    """
    load_dotenv()  # Load the variables from the .env file
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("Invalid or missing API key. Please check your .env file.")
    return api_key


class APIError(Exception):
    """Custom exception for handling API-related errors."""
    pass


class MovieInfoDownloader:
    """
        A class to fetch movie information using the OMDb API.

        Attributes:
            api_url (str): URL of the API endpoint for fetching movie information.
            api_key (str): The API key required for API requests.
    """
    def __init__(self, api_url: str = None) -> None:
        """
            Initialize the MovieInfoDownloader with an API URL and key.

            Args:
                api_url (str, optional): API URL for fetching movie information. Defaults to OMDb API.
        """
        self._api_url = api_url or "http://www.omdbapi.com/"
        self._api_key = load_api_key()

    def fetch_movie_data(self, title: str) -> dict:
        """
            Fetch detailed information about a movie by its title.

            Args:
                title (str): Title of the movie to search for.

            Returns:
                dict: A dictionary containing the movie's title, year, IMDb rating, poster URL,
                          IMDb link, and an optional notes field.

            Raises:
                APIError: If there is an issue with the request, response, or data processing.
        """

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(HTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.5'
        }

        try:
            response = requests.get(
                f"{self._api_url}?t={title}&apikey={self._api_key}",
                headers=headers,
                timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'Title' not in data or 'imdbID' not in data:
                raise APIError(f"Incomplete data received for movie: {title}")

            return {data.get('Title'): {
                    'Title': data.get('Title'),
                    'Year': data.get('Year'),
                    'Rating': data.get('imdbRating'),
                    'Poster': data.get('Poster'),
                    'IMDB Link': f"https://www.imdb.com/title/{data.get('imdbID')}/",
                    'Notes': ""}
                    }

        except (HTTPError, ConnectionError, Timeout) as req_err:
            raise APIError(f"Request error occurred: {req_err}")
        except ValueError as json_err:
            raise APIError(f"Error parsing JSON: {json_err}")
        except RequestException as err:
            raise APIError(f"Error fetching movie info: {err}")
