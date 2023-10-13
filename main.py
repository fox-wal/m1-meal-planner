#==============#
# MEAL PLANNER #
#==============#

from recipe import Recipe
from enum import Enum
from settings import *
from format import *

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
    if menu.__len__() == 0:
        print(ERROR_NO_MENU)
        return

    # Display each item in the menu preceded by an index (starting from 1).
    for i in range(0, menu.__len__()):
        print(f"{i + 1}. {menu[i]}")

def display_selection_menu(menu: list[str]) -> int:
    """
    Displays a menu and prompts user to select an item.

    Returns::
        The index of the chosen item, or the exit value if the user entered the exit character.
    """
    display_menu(menu)
    return user_selects_menu_item(menu.__len__())

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

#--------------#
# View Recipes #
#--------------#

def filter_recipes(recipes: list[Recipe], check_include_recipe: function(Recipe)) -> list[int]:
    """
    Add the index of each recipe that satisfies the given filter condition to a list.

    Args:
        recipes: The recipes to be filtered.
        check_include_recipe: Used to determine whether a given recipe should be included in the resulting list.
    
    Returns:
        Indexes of recipes that satisfy the condition(s) checked in check_include_recipe.
    """
    filtered_recipe_indexes = []
    for i in range(recipes.__len__()):
        if check_include_recipe(recipes[i]):
            filtered_recipe_indexes.append(i)

def load_files(path: str) -> list[str]:
    """
    Load all configuration and data files.

    Args:
        path: The absolute or relative path of the file to load.

    Returns:
        The file at the specified path as a list of lines.
    """
    # TODO: write file loading function
    load_recipes()
    pass

def load_recipes() -> list[Recipe]:
    """
    Load and parse the recipe file.

    Returns:
        The recipes from the file.
    """
    # TODO: write recipe loading function
    RECIPE_PATH = "recipes.json"
    pass

def check_contains_tags(recipe: Recipe, tags: list[str], union: bool) -> bool:
    """
    Check whether `recipe` contains the given `tags`.

    Args:
        recipe: The recipe to check.
        tags: Will check whether `recipe` contains these.
        union: Determines whether to check that `recipe` contains *at least one* of the `tags` (True) or *all* of them (False).
    
    Returns:
        True if it does.
        False if it does not.
    """
    contains_at_least_one_tag = False
    contains_all_tags = True
    for tag in tags:
        if recipe.get_tags().__contains__(tag):
            contains_at_least_one_tag = True
        else:
            contains_all_tags = False
    return contains_all_tags or (contains_at_least_one_tag and union)

def check_contains_keywords(recipe: Recipe, search_terms: list[str], union: bool) -> bool:
    """
    Check whether `recipe` contains the given `search_terms`.

    Args:
        recipe: The recipe to check.
        search terms: Will check whether `recipe` contains these.
        union: Determines whether to check that `recipe` contains *at least one* of the `search_terms` (True) or *all* of them (False).
    
    Returns:
        True if it does.
        False if it does not.
    """
    contains_at_least_one_keyword = False
    contains_all_keywords = True
    for keyword in search_terms:
        if recipe.get_keywords().__contains__(keyword):
            contains_at_least_one_keyword = True
        else:
            contains_all_keywords = False
    return contains_all_keywords or (contains_at_least_one_keyword and union)

def check_satisfies_filters(recipe: Recipe, filters: list[FilterConditions]) -> bool:
    """
    Check the given `recipe` against every given filter.

    Args:
        recipe: The recipe to be checked.
        filters: The filter conditions to check whether the `recipe` satisfies.

    Returns:
        True if the `recipe` satisfies every filter.
        False if it does not.
    """
    return ((settings.active_filters.__contains__(FilterConditions.TAGS)      and check_contains_tags(recipe, settings.active_tags, settings.tag_union))
        and (settings.active_filters.__contains__(FilterConditions.SEARCH)    and check_contains_keywords(recipe, settings.search_terms, settings.keyword_search))
        and (settings.active_filters.__contains__(FilterConditions.PREP_TIME) and (recipe._prep_time <= settings.max_prep_time)))

def display_recipe(recipe: Recipe):
    """Display all of the given recipe's attributes."""
    print(recipe.format_title())
    print(format_heading("Ingredients"))
    print(recipe.format_ingredients())
    print(format_heading("Method"))
    print(recipe.format_method())
    print("Tags:", recipe.format_tags())

class FilterMenuOptions(Enum):
    SORT_BY = 0
    SEARCH_TERMS = 1
    TAGS = 2
    MAX_PREPARATION_TIME = 3

def sort_recipes(recipes: list[Recipe], compare: function) -> list[Recipe]:
    """
    Sort the `recipes` according to the `compare` function.
    
    Args:
    compare (Recipe, Recipe) -> int: If this returns a value < 0, this means that the left value comes before the right value.

    Returns:
        A list of recipes sorted based on the `compare` function.
    """
    if recipes.__len__() == 1:
        return recipes
    mid = recipes.__len__() // 2
    left: list[Recipe] = sort_recipes(recipes[:mid], compare)
    right: list[Recipe] = sort_recipes(recipes[mid:], compare)
    result: list[Recipe]
    i: int = 0
    j: int = 0
    while (i + j) < (left.__len__() + right.__len__()):
        if compare(left[i], right[j]) < 0:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    while i < left.__len__():
        result.append(left[i])
        i += 1
    while j < right.__len__():
        result.append(right[j])
        j += 1
    return result

def name(variable) -> str:
    """Returns: the name of the given variable."""
    return f'{variable=}'.split('=')[0]

def view_recipes(recipes: list[Recipe]):
    """The view recipes menu option: select a recipe to view it."""
    # TODO: break down this function
    print(settings.generate_filter_settings_output(NO_MAX_PREP_TIME))

    # User decides whether to edit sort/filter settings.
    choice = input("Would you like to change these sorting/filtering settings? [Y/N]")

    if choice.upper() == "Y":
        # User selects a sort/filter item to edit
        choice = display_selection_menu(map(format_var_name, FilterMenuOptions._member_names_))

        match choice:
            case FilterMenuOptions.SORT_BY:
                choice = display_selection_menu(map(format_var_name, SortBys._member_names_))
                if choice != EXIT_VALUE:
                    settings.sort_by = choice
            
            case 1:
                user_input = input("Search: ")
                if user_input != "":
                    settings.search_terms = user_input.split(' ')
            
            # The cursor jumps from line to line.
            # - [Enter] = keep the same
            # - a = add
            # - r = remove
            # - c = clear all
            case 2:
                MAX_TAG_LENGTH = 20
                print("Command  | Function")
                print("---------|-------------------------------------------------")
                print("a        | activate current tag")
                print("d        | deactivate)")
                print("da       | deactivate all tags")
                print("1        | activate the current tag and deactivate the rest")
                print("anything | do nothing")
                print("else     |")
                print()
                print(f"{'Tag'.ljust(MAX_TAG_LENGTH)}    {'Status'.ljust(MAX_SYMBOL_LENGTH)}    Command")
                for tag in settings._all_tags:
                    # NOTE: max char amount for tag is:
                    MAX_SYMBOL_LENGTH = "Active".__len__()
                    if active_tags.__contains__(tag):
                        status = "Active"
                    else:
                        status = ""
                    user_input = input(f"{tag.ljust(MAX_TAG_LENGTH)}    {status.ljust(MAX_SYMBOL_LENGTH)}    ")
                    match user_input:
                        case "a":
                            if status != "Active":
                                active_tags.append(tag)
                        case "d":
                            if status == "Active":
                                active_tags.remove(tag)
                        case "da":
                            active_tags.clear()
                        case "1":
                            active_tags = [tag]
            
            # For max prep time, user enters a value in minutes, or 0 to remove the constraint.
            case 3:
                if max_prep_time == 0:
                    output += "none"
                else:
                    output += format_time(max_prep_time)
                print("Current max prep time:", output)
                value = input_int(f"Enter new max prep time in minutes (or {EXIT_CHAR} to exit): ", 0)
                if value != EXIT_VALUE:
                    max_prep_time = value
                
        # TODO: remove union and intersect variations in enum and create a separate variable for it

    def compare_attribute(left: Recipe, right: Recipe, attribute: str) -> int:
        """
        Compare the given `attribute` of the two given recipes.

        Returns:
          - -1 if `left` < `right`
          - 0 if `left` = `right`
          - 1 if `left` > `right`
        """
        LESS_THAN = -1
        EQUAL = 0
        GREATER_THAN = 1
        if left.__getattribute__(attribute) < right.__getattribute__(attribute):
            return LESS_THAN
        elif left.__getattribute__(attribute) == right.__getattribute__(attribute):
            return EQUAL
        else:
            return GREATER_THAN

    compare_functions = {
        SortBys.NAME : lambda left, right: compare_attribute(left, right, f'{Recipe._name=}'.split('=')[0]),
        SortBys.PREP_TIME : lambda left, right: compare_attribute(left, right, f'{Recipe._prep_time=}'.split('=')[0])
    }

    # Filter recipes
    check_recipe_satisfies_filters = lambda recipe: check_satisfies_filters(recipe)
    filtered_recipes = filter_recipes(recipes, check_recipe_satisfies_filters)
    filtered_recipes = sort_recipes(filtered_recipes, compare_functions[settings.sort_by])
    
    # Display recipes (filtered)
    while recipe_to_display != -1:
        recipe_to_display = display_selection_menu([recipes[i].get_name() for i in filtered_recipes])
        if recipe_to_display == -1:
            break
        display_recipe(recipes[filtered_recipes[recipe_to_display]])
        input("Enter any key to exit: ")

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
choice = user_selects_menu_item(MAIN_MENU.__len__())
match choice:
    case MenuOptions.VIEW_RECIPES:
        view_recipes(recipes)
    # case Menu_options.ADD_RECIPES:
    #     add_recipes(recipes)
    # case Menu_options.ADD_UNITS:
    #     add_units(units)
    # case Menu_options.VIEW_MEAL_PLANS:
    #     view_meal_plans(meal_plans)
    # case Menu_options.CREATE_MEAL_PLANS:
    #     create_meal_plans(meal_plans)
    case MenuOptions.EXIT:
        print("Exiting...")
    case other:
        print(f"[{MAIN_MENU[choice]}] selected.")
