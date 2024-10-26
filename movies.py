import sys
from analytics import *
from crud import *


def exit_command():
    """
    Exits the program by printing a farewell message and terminating the process.
    """
    print("Bye!")
    sys.exit(0)


def display_menu(menu_entries):
    """
    Displays the menu to the user.
    Args:
        menu_entries (list): A list of tuples where each tuple contains a menu option description
                             and the corresponding function to call.
    """
    print("\nMenu:")
    for index, (description, _) in enumerate(menu_entries):
        print(f"{index}. {description}")
    print()


def get_user_choice(menu_entries):
    """
    Prompts the user to select a menu option and ensures valid input.
    Args:
        menu_entries (list): A list of menu entries to choose from.
    Returns:
        int: The index of the chosen menu entry, if valid or None, if invalid
    """
    user_input = input(f"Enter choice (0-{len(menu_entries) - 1}): ").strip()
    if user_input:
        try:
            choice = int(user_input)
            if choice in range(len(menu_entries)):
                return choice
        except ValueError:
            pass
    print(f"Invalid choice: [{user_input}]")
    return None


def main():
    """
    Main function to run the Movies Database application.

    It displays a menu to the user, allowing them to perform various actions
    such as listing movies, adding, deleting, updating, showing statistics,
    and more. The user input is taken and the corresponding function is
    called based on the choice.
    """
    menu_entries = [
        ("Exit", exit_command),
        ("List movies", list_movies),
        ("Add movie", add_movie),
        ("Delete movie", delete_movie),
        ("Update movie", update_movie),
        ("Stats", show_statistics),
        ("Random movie", random_movie),
        ("Search movie", fuzzy_search),
        ("Movies sorted by rating", sorted_by_rating),
        ("Movies sorted by year", sorted_by_year),
        ("Filter movies", filtered_movies)
    ]

    print("********** My Movies Database **********")

    while True:
        display_menu(menu_entries)
        choice = get_user_choice(menu_entries)
        if choice is None:
            continue
        print()
        menu_entries[choice][1]()
        input("\nPress Enter to continue")


if __name__ == "__main__":
    main()
