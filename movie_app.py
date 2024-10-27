import sys
from commands.analytics import Analytics
from commands.crud import Crud


class MovieApp:

    def __init__(self, storage):
        self._storage = storage
        self._crud = Crud(self._storage)
        self._analytics = Analytics(self._storage)
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
            ("Generate website", self._generate_website)
        ]

    @staticmethod
    def exit_command():
        """
        Exits the program by printing a farewell message and terminating the process.
        """
        print("Bye!")
        sys.exit(0)

    def display_menu(self):
        """
        Displays the menu to the user.

        """
        print("\nMenu:")
        for index, (description, _) in enumerate(self.menu_entries):
            print(f"{index}. {description}")
        print()

    def get_user_choice(self):
        """
        Prompts the user to select a menu option and ensures valid input.

        Returns:
            int: The index of the chosen menu entry, if valid or None, if invalid
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

    def _generate_website(self):
        pass

    def run(self):
        """Function to run the movie app"""
        print("********** My Movies Database **********")
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            if choice is None:
                continue
            print()
            self.menu_entries[choice][1]()
            input("\nPress Enter to continue")
