#
# MEAL PLANNER
#

from recipe import recipe
from enum import Enum

# Display an error message.
def print_error(error_message: str):
    print("Error:", error_message)

# Display a menu with an index (starting from 1) before each item.
def display_menu(menu: list[str]):
    ERROR_NO_MENU = "No menu to display."

    # Check if there are any items in the menu.
    if menu.__len__() == 0:
        print(ERROR_NO_MENU)
        return

    # Display each item in the menu preceded by an index (starting from 1).
    for i in range(0, menu.__len__()):
        print(f"{i + 1}. {menu[i]}")

# Prompt the user to enter an integer to select an item from a menu until they
# enter a valid number.
# >> Return: the index selected, or -1 if the user entered "X".
def user_selects_item_from_menu(menu_size: int) -> int:
    EXIT_CHAR = "X"
    EXIT_VALUE = -1

    MIN = 1
    MAX = menu_size

    PROMPT = f"Select an item from the menu using the index. Enter {EXIT_CHAR} to exit.\n"

    ERROR_GENERIC =  "Invalid selection."
    ERROR_OUT_OF_RANGE = f"Please enter a whole number between {MIN} and {MAX}."
    ERROR_NOT_INTEGER = "Please ensure you enter a whole number."

    # Ask user for input.
    print(PROMPT)

    # Continue prompting user for input using relevant error messages until they
    # enter a valid integer within the appropriate range.
    valid = False
    while not valid:
        try:
            str_input = input()
            selection = int(str_input)
            valid = (MIN <= selection) and (selection <= MAX)
            if not valid:
                print_error(ERROR_OUT_OF_RANGE)
        except ValueError:
            # If the user entered the exit character, return the exit value so the
            # user can exit the menu.
            if str_input.upper() == EXIT_CHAR:
                return EXIT_VALUE
            # Otherwise, the user must have entered an invalid non-integer.
            print_error(ERROR_NOT_INTEGER)
        # except:
        #     print_error(ERROR_GENERIC)
    return selection - 1

MAIN_MENU = [
    "View recipes",
    "Add/edit recipe",
    "Add/edit units",
    "View meal plans",
    "Create/edit meal plan",
]

#
# Display Main Menu
#
def display_main_menu():
    display_menu(MAIN_MENU)
    choice = user_selects_item_from_menu(MAIN_MENU.__len__())
    if choice != -1:
        # TODO: Go to the appropriate place
        print(f"[{MAIN_MENU[choice]}] selected.")
    else:
        print("Exiting...")

#
# View Recipes
#

# Display the names of all the recipes, subject to the filter conditions.
def display_recipes(recipes: list, filter_condition: function(recipe) = None) -> bool:
    if recipes.__len__() == 0:
        return False

    recipes_have_been_displayed = True

    # Check if there is a filter. If not, we can save some time by not checking
    # whether it's met in each iteration.
    if filter_condition is None:
        for recipe in recipes:
            print(recipe.get_name())
    else:
        recipes_have_been_displayed = False
        for recipe in recipes:
            if filter_condition(recipe):
                print(recipe.get_name())
                recipes_have_been_displayed = True
        return recipes_have_been_displayed

class filter_conditions(Enum):
    CONTAINS_TAGS_UNION = 0,
    CONTAINS_TAGS_INTERSECT = 1,
    CONTAINS_KEYWORDS_UNION = 2, # Use 'or' in condition checking
    CONTAINS_KEYWORDS_INTERSECT = 3, # Use 'and' in condition checking
    DURATION_LESS_THAN = 4

all_tags: list[str]

def check_contains_tags(recipe: recipe, tags: list[str], union: bool = True) -> bool:
    contains_at_least_one_tag = False
    contains_all_tags = True
    for tag in tags:
        if recipe.get_tags().__contains__(tag):
            contains_at_least_one_tag = True
        else:
            contains_all_tags = False
    return contains_all_tags or (contains_at_least_one_tag and union)

def check_contains_keywords(recipe: recipe, keywords: list[str], union: bool = True) -> bool:
    contains_at_least_one_keyword = False
    contains_all_keywords = True
    for keyword in keywords:
        if recipe.get_keywords().__contains__(keyword):
            contains_at_least_one_keyword = True
        else:
            contains_all_keywords = False
    return contains_all_keywords or (contains_at_least_one_keyword and union)

# Check the given recipe against each active filter.
# >> Return: True if the recipe satisfies every active filter.
#            False if it does not.
def apply_selected_filters(recipe: recipe, filter_on: dict[filter_conditions, bool],
                           tags: list[str], keywords: list[str], max_duration: int) -> bool:
    return ((filter_on[filter_conditions.CONTAINS_TAGS_UNION]         and check_contains_tags(recipe, tags, union=True)) 
        and (filter_on[filter_conditions.CONTAINS_TAGS_INTERSECT]     and check_contains_tags(recipe, tags, union=False))
        and (filter_on[filter_conditions.CONTAINS_KEYWORDS_UNION]     and check_contains_keywords(recipe, keywords, union=True))
        and (filter_on[filter_conditions.CONTAINS_KEYWORDS_INTERSECT] and check_contains_keywords(recipe, keywords, union=False))
        and (filter_on[filter_conditions.DURATION_LESS_THAN]          and (recipe.get_duration <= max_duration)))

# Set all values to the given default value (without changing the keys).
def reset_filters(active_filters: dict[filter_conditions, bool], default_value: bool = False):
    for key in active_filters.keys():
        active_filters[key] = default_value
    return active_filters

# The view recipes menu option
# Apply filters
# Search
# Select a recipe to view it
def view_recipes():
    # TODO: Load recipes from file
    recipes = list[recipe]
    display_recipes(recipes)
    # TODO: Allow user to enter filter options --> perhaps do this in settings

    chosen_filters: list[filter_conditions] = []
    chosen_tags = list[int] = []
    chosen_keywords: list[str] = []
    chosen_duration: int = [] # Max duration

    filter_on = {
        filter_conditions.CONTAINS_TAGS_UNION : False,
        filter_conditions.CONTAINS_TAGS_INTERSECT : False,
        filter_conditions.CONTAINS_KEYWORDS_UNION : False,
        filter_conditions.CONTAINS_KEYWORDS_INTERSECT : False,
        filter_conditions.DURATION_LESS_THAN : False
    }

    # Activate chosen filters
    filter_on = reset_filters()

    for filter in chosen_filters:
        filter_on[filter] = True

    # Display recipes (filtered)
    check_recipe_satisfies_filters = lambda recipe: apply_selected_filters(recipe, filter_on, chosen_tags, chosen_keywords, chosen_duration)
    display_recipes(recipes, check_recipe_satisfies_filters)
