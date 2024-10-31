import os
from pathlib import Path
from storage.istorage import IStorage


class WebGenerator:
    """
        A class to generate a website for displaying movies.

        This class loads an HTML template, serializes movie data,
        and generates an HTML file with a movie grid based on the data.
    """

    project_dir = Path(__file__).parent.parent
    template_path = os.path.join(project_dir,
                                 "_static", "index_template.html")
    new_index_path = os.path.join(project_dir,
                                  "_static", "index.html")

    def __init__(self, movies_data: IStorage, new_path=new_index_path):
        """
            Initialize the WebGenerator with movie data and an output path.

            Args:
                movies_data (object): The data containing movie information.
                new_path (str, optional): The path to save the generated HTML file.
                                          Defaults to `new_index_path`.
        """
        self.movies = movies_data
        self.new_path = new_path

    def generate_website(self) -> None:
        """
            Generate the HTML website for the movie list.

            This method loads the template, inserts serialized movie data into the
            template, and writes the updated HTML to the specified output path.
        """

        template = self.load_template(WebGenerator.template_path)
        serialized_data = self.serialize_movies()
        new_html = template.replace('__TEMPLATE_MOVIE_GRID__', serialized_data)
        self.write_file(self.new_path, new_html)

    @staticmethod
    def load_template(path: str) -> str:
        """
            Load and return the content of a template file.

            Opens the specified file in read mode, reads its content, and returns it.
            Raises an error if the file is not found or if it's empty.

            Args:
                path (str): The path to the file.

            Returns:
                str: The content of the file as a string.

            Raises:
                FileNotFoundError: If the file does not exist.
                ValueError: If the file is empty.
        """
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                if not content:
                    raise ValueError(f"Error: The file '{path}' is empty.")
                return content
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file '{path}' was not found.")

    def serialize_movies(self) -> str:
        """
            Serialize the movie data into an HTML list format.

            This method generates HTML list items for each movie with details such
            as title, year, rating, and notes. If notes are present, they are added
            as a tooltip.

            Returns:
                str: An HTML string representing the movie list.
        """
        output = ''
        movies = self.movies.get_movies()
        for movie, details in movies.items():
            imdb_link = details.get('IMDB Link', '#')
            poster_url = details.get('Poster', '')
            year = details.get('Year', 'N/A')
            rating = details.get('Rating', 'N/A')
            notes = details.get('Notes', '')
            # Conditionally add the tooltip span if there are notes
            notes_html = f'<span class="tooltiptext">{notes}</span>' if notes else ''

            output += f"""
            <li>
                <div class="movie">
                    <a href="{imdb_link}" target="_blank">
                        <img src="{poster_url}" alt="{movie}" class="movie-poster"/>
                    </a>
                    <div class="movie-title">{movie}</div>
                    <div class="movie-year">({year})</div>
                    <div class="movie-rating">Rating: {rating}</div>
                    <div class="movie-notes">{notes_html}</div>
                </div>
            </li>
            """

        return output

    @staticmethod
    def write_file(path, content):
        """
            Write the given content to a file.

            Opens the specified file in write mode, writes the provided content,
            and prints a success message.

            Args:
                path (str): The file path where content should be saved.
                content (str): The content to write to the file.

            Raises:
                IOError: If there is an issue with writing to the file.
        """
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"Website was successfully generated at {path}.")
        except IOError as e:
            print(f"Failed to write to file '{path}': {e}")