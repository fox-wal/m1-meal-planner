#==============#
# MEAL PLANNER #
#==============#

from recipe import Recipe
from enum import Enum
from settings import *
from format import *
from view_recipes import view_recipes
from add_edit_recipe import add_edit_recipe

# Global variables
EXIT_CHAR = "X"
EXIT_VALUE = -1
NO_MAX_PREP_TIME = "no max"
settings: Settings = Settings([], 0, SortBys.NAME, [], [])

#---------------------------#
# General-Purpose Functions #
#---------------------------#
def display_menu(menu: list[str]):
    """
    Displays a menu with an index (starting at 1) before each item.

    Args:
        menu: The menu to be displayed.
    """

    ERROR_NO_MENU = "No menu to display."

    # Check if there are any items in the menu.
    if len(menu) == 0:
        print(ERROR_NO_MENU)
        return

    # Display each item in the menu preceded by an index (starting from 1).
    for i in range(0, len(menu)):
        print(f"{i + 1}. {menu[i]}")

def display_selection_menu(menu: list[str]) -> int:
    """
    Displays a menu and prompts user to select an item.

    Returns::
        The index of the chosen item, or the exit value if the user entered the exit character.
    """
    display_menu(menu)
    return user_selects_menu_item(len(menu))

def input_int(prompt: str = "", min: int = None, max: int = None) -> int:
    """
    Prompts the user to enter a valid number or the exit character until they do so.

    Args:
        prompt: The initial prompt displayed to the user.
        min: The (inclusive) minimum value the user should enter.
        max: The (inclusive) maximum value the user should enter.

    Returns:
        The validated user input, or the exit value if the user selected the exit character.
    """
    
    ERROR_OUT_OF_RANGE = f"Please enter a whole number between {min} and {max}."
    ERROR_NOT_INTEGER = "Please ensure you enter a whole number."

    valid = False
    print(prompt)

    # Continue prompting user for input using relevant error messages until they
    # enter a valid integer within the appropriate range.
    valid = False
    while not valid:
        try:
            str_input = input()
            number = int(str_input)
            valid = ((min is None) or (min <= number)) and ((max is None) or (number <= min))
            if not valid:
                print(format_error(ERROR_OUT_OF_RANGE))
        except ValueError:
            # If the user entered the exit character, return the exit value so the
            # user can exit the menu.
            if str_input.upper() == EXIT_CHAR:
                return EXIT_VALUE
            # Otherwise, the user must have entered an invalid non-integer.
            print(format_error(ERROR_NOT_INTEGER))
    return number
     
def user_selects_menu_item(menu_size: int) -> int:
    """
    Prompt the user to enter a valid index until they do so.
    
    Args:
        menu_size: The number of items in the menu from which the user is making a selection.

    Returns:
        The index of the chosen item, or the exit value if the user entered the exit character.
    """
    MIN = 1
    MAX = menu_size - 1

    PROMPT = f"Select an item from the menu using the index. Enter {EXIT_CHAR} to exit.\n"

    selection = input_int(PROMPT, MIN, MAX)

    return selection - 1

#-------------------#
# Main Code Section #
#-------------------#

# Load files
recipes: list[Recipe]
load_files(recipes)

# Main menu
class MenuOptions(Enum):
    VIEW_RECIPES = 0
    ADD_RECIPES = 1
    ADD_UNITS = 2
    VIEW_MEAL_PLANS = 3
    CREATE_MEAL_PLANS = 4
    EXIT = -1
MAIN_MENU = [
    "View recipes",
    "Add/edit recipe",
    "Add/edit units",
    "View meal plans",
    "Create/edit meal plan",
]
display_menu(MAIN_MENU)
choice = user_selects_menu_item(len(MAIN_MENU))
match choice:
    case MenuOptions.VIEW_RECIPES:
        view_recipes(recipes)
    case MenuOptions.ADD_RECIPES:
        add_recipes(recipes)
    case MenuOptions.ADD_UNITS:
        add_units(units)
    case MenuOptions.VIEW_MEAL_PLANS:
        view_meal_plans(meal_plans)
    case MenuOptions.CREATE_MEAL_PLANS:
        create_meal_plans(meal_plans)
    case MenuOptions.EXIT:
        print("Exiting...")
    case other:
        print(f"[{MAIN_MENU[choice]}] selected.")
