import sys
from commands.analytics import Analytics
from commands.crud import Crud
from commands.web_generator import WebGenerator
from storage.istorage import IStorage


class MovieApp:
    """
        A console-based application for managing a movie database, providing a menu interface
        for CRUD operations, analytics, and web generation.

        This class serves as the main entry point for interacting with a movie database,
        supporting operations to list, add, delete, and update movies, as well as analytics
        functions like statistics, sorting, filtering, and generating a website view of the
        movie database.

        Attributes:
            _storage (object): An object that interfaces with the movie database storage,
                               such as a JSON or database file.
            _crud (Crud): An instance of the Crud class for handling create, read, update,
                          and delete operations.
            _analytics (Analytics): An instance of the Analytics class for data analysis
                                    and statistics.
            _webgenerator (WebGenerator): An instance of the WebGenerator class for
            generating a website.
            menu_entries (list): A list of tuples, each containing a description and a
                                function reference for menu options available to the user.

        Methods:
            exit_command(): Terminates the application.
            display_menu(): Prints the available menu options.
            get_user_choice(): Prompts the user for a menu selection and validates the input.
            run(): Starts the application loop, displaying the menu and executing the chosen
                   commands.
    """

    def __init__(self, storage: IStorage):
        """
            Initializes the MovieApp instance with provided storage and sets up dependencies.

            Args:
                storage (object): The storage backend for the movie database, providing methods
                to manage movies.
        """
        self._storage = storage
        self._crud = Crud(self._storage)
        self._analytics = Analytics(self._storage)
        self._webgenerator = WebGenerator(self._storage)
        self.menu_entries = [
            ("Exit", self.exit_command),
            ("List movies", self._crud.list_movies),
            ("Add movie", self._crud.add_movie),
            ("Delete movie", self._crud.delete_movie),
            ("Update movie", self._crud.update_movie),
            ("Stats", self._analytics.show_statistics),
            ("Random movie", self._analytics.random_movie),
            ("Search movie", self._analytics.fuzzy_search),
            ("Movies sorted by rating", self._analytics.sorted_by_rating),
            ("Movies sorted by year", self._analytics.sorted_by_year),
            ("Filter movies", self._analytics.filtered_movies),
            ("Generate website", self._webgenerator.generate_website)
        ]

    @staticmethod
    def exit_command():
        """
            Exits the program by printing a farewell message and terminating the process.

            This method is called when the user selects the "Exit" option from the menu.
        """
        print("Bye!")
        sys.exit(0)

    def display_menu(self):
        """
            Displays the available menu options to the user.

            This method iterates through the `menu_entries` list and prints each option
            with its corresponding index number.
        """
        print("\nMenu:")
        for index, (description, _) in enumerate(self.menu_entries):
            print(f"{index}. {description}")
        print()

    def get_user_choice(self):
        """
            Prompts the user to select a menu option and ensures valid input.

            Returns:
                int: The index of the chosen menu entry, if valid; None if invalid.

            This method accepts the user's choice, validates that it is within the range
            of available options, and returns the choice if valid. If invalid, an error
            message is displayed and None is returned.
        """
        user_input = input(f"Enter choice (0-{len(self.menu_entries) - 1}): ").strip()
        if user_input:
            try:
                choice = int(user_input)
                if choice in range(len(self.menu_entries)):
                    return choice
            except ValueError:
                pass
        print(f"Invalid choice: [{user_input}]")
        return None

    def run(self):
        """
            Starts the main loop of the movie app, displaying the menu and executing selected
            commands.

            This method continuously displays the menu, prompts the user for a choice, and executes
            the corresponding function until the user selects "Exit." After each action, it pauses
            for user input to continue.
        """
        print("********** My Movies Database **********")
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            if choice is None:
                continue
            print()
            self.menu_entries[choice][1]()
            input("\nPress Enter to continue")
