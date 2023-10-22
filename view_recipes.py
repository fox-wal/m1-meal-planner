#--------------#
# View Recipes #
#--------------#

from main import display_selection_menu, input_int
from recipe import Recipe
from enum import Enum
from settings import Settings, FilterConditions, SortBys
from format import format_heading, format_time, format_var_name

def filter_recipes(recipes: list[Recipe], check_include_recipe: function(Recipe)) -> list[Recipe]:
    """
    Add each recipe that satisfies the given filter condition to a list.

    Args:
        recipes: The recipes to be filtered.
        check_include_recipe: Used to determine whether a given recipe should be included in the resulting list.
    
    Returns:
        List of recipes that satisfy the condition(s) checked in `check_include_recipe`.
    """
    

    filtered_recipes = []

    for r in recipes:
        if check_include_recipe(recipes[r]):
            filtered_recipes.append(r)

    return filtered_recipes

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

def deep_search(recipe: Recipe, search_attribute: str, search_terms: list[str], union: bool):
    """
    Check whether `recipe` contains the given `search_terms`.

    Args:
        recipe: The `recipe` to check.
        search_attribute: Where to look for the `search_terms`.
        search_terms: Will check whether `recipe` contains these.
        union: Determines whether to check that `recipe` contains *at least one* of the `search_terms` (True) or *all* of them (False).
    
    Returns:
        True if it does.
        False if it does not.
    """

    count = 0

    for term in search_terms:
        if term in recipe.__getattribute__(search_attribute):
            count += 1

    return (count > 0) and ((count == len(search_terms)) or union)

def check_satisfies_filters(recipe: Recipe, settings: Settings) -> bool:
    """
    Check the given `recipe` against every given filter.

    Args:
        recipe: The recipe to be checked.
        filters: The filter conditions to check whether the `recipe` satisfies.

    Returns:
        True if the `recipe` satisfies every filter.
        False if it does not.
    """

    return (((FilterConditions.TAGS      in settings.active_filters) and deep_search(recipe, "_tags", settings.active_tags, settings.tag_union))
        and ((FilterConditions.SEARCH    in settings.active_filters) and deep_search(recipe, "_search_terms", settings.search_terms, settings.keyword_search))
        and ((FilterConditions.PREP_TIME in settings.active_filters) and (recipe.get_prep_time() <= settings.max_prep_time)))

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

    if len(recipes) == 1:
        return recipes
    
    # Split

    mid = len(recipes) // 2
    left: list[Recipe] = sort_recipes(recipes[:mid], compare)
    right: list[Recipe] = sort_recipes(recipes[mid:], compare)

    result: list[Recipe] = []
    
    # Merge

    i: int = 0
    j: int = 0
    
    while (i + j) < (len(left) + len(right)):
        if compare(left[i], right[j]) < 0:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Finish off
    
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    
    return result

def name(variable) -> str:
    """
    Returns: the name of the given variable.
    """
    return f'{variable=}'.split('=')[0]

def display_table(rows: list[str], contains_header: bool):
    '''
    Display a table.

    Args:
        rows: Rows of the table.
        contains_header: If True: will display a line beneath the first row.
    '''
    
    print(rows[0])

    # Header
    if contains_header:
        print("".ljust(len(rows[0]), "-"))

    # Contents
    for row in rows[1:]:
        print(row)

def format_table(data: list[list[str]], delimiter: str) -> list[str]:
    '''
    Format the given data as a table.

    Args:
        data: List of rows, each of which is a list of fields.
        delimiter: Separates columns from one another.

    Returns:
        The given `data` formatted as rows with each field padded and separated
        by the `delimiter`.
    '''

    # Get max length of the values in each column.

    max_lengths: list[int]

    for row in data:
        for i in range(len(row)):
            if len(row[i]) > max_lengths[i]:
                max_lengths[i] = len(row[i])
    
    # Format rows.

    table: list[str]

    for row in data:
        padded_fields = [ row[i].ljust(max_lengths[i]) for i in range(row) ]
        table.append(delimiter.join(padded_fields))

    return table

def format_tag_table_row(fields: list[str], max_tag_length: int, delimiter: str = "    ") -> str:
    return delimiter.join([field.ljust(max_tag_length) for field in fields])

class Commands(Enum):
    ACTIVATE_CURRENT_TAG = "a"
    DEACTIVATE_CURRENT_TAG = "d"
    DEACTIVATE_ALL_TAGS = "da"
    ACTIVATE_ONLY_THIS_TAG = "1"

def edit_tags(tags: list[str], active_tags: list[str]):
    '''
    Allow user to edit which tags are currently active.
    '''

    MAX_TAG_LENGTH = 20
    INSTRUCTIONS = [
        ["Command",                       "Function"],
        [Commands.ACTIVATE_CURRENT_TAG,   "Activate this tag"],
        [Commands.DEACTIVATE_CURRENT_TAG, "Deactivate this tag"],
        [Commands.DEACTIVATE_ALL_TAGS,    "Deactivate all tags"],
        [Commands.ACTIVATE_ONLY_THIS_TAG, "Activate the current tag and deactivate the rest"]
    ]

    tag_table_headers = [ "Tag", "Active?", "Command" ]
    DELIMITER = "    "
    is_active: bool
    prompt = format_tag_table_row(tag_table_headers[:-1], MAX_TAG_LENGTH, DELIMITER) + DELIMITER

    # Display instructions

    display_table(format_table(INSTRUCTIONS, " | "), True)
    print(format_tag_table_row(tag_table_headers))

    # Edit tags

    for tag in tags:

        is_active = tag in active_tags
        command = input(prompt)

        match command:
            case "a":
                if not is_active:
                    active_tags.append(tag)
            case "d":
                if is_active:
                    active_tags.remove(tag)
            case "da":
                active_tags.clear()
            case "1":
                active_tags.clear()
                active_tags.append(tag)

def change_max_prep_time(settings: Settings):
    '''
    User enters max prep time and it is updated in the `settings`.
    '''
    
    output: str = "Current max prep time: "

    if settings.max_prep_time == 0:
        output += "none"
    else:
        output += format_time(settings.max_prep_time)

    print(output)

    value = input_int(f"Enter new max prep time in minutes (or {EXIT_CHAR} to exit): ", 0)
    if value != EXIT_VALUE:
        settings.max_prep_time = value

def edit_sort_and_filter_settings(settings: Settings):
    """
    Allow user to edit sort and filter settings.
    """
    
    # User selects a sort/filter item to edit
    choice = display_selection_menu(map(format_var_name, FilterMenuOptions._member_names_))

    match choice:
        case FilterMenuOptions.SORT_BY:
            choice = display_selection_menu(map(format_var_name, SortBys._member_names_))
            if choice != EXIT_VALUE:
                settings.sort_by = choice
        
        case FilterMenuOptions.SEARCH_TERMS:
            user_input = input("Search [separate search terms by spaces]: ")
            if user_input != "":
                settings.search_terms = user_input.split(" ")
        
        case FilterMenuOptions.TAGS:
            edit_tags(settings.all_tags, settings.active_tags)

        # For max prep time, user enters a value in minutes, or 0 to remove the constraint.
        case FilterMenuOptions.MAX_PREPARATION_TIME:
            change_max_prep_time(settings)

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

def view_recipes(recipes: list[Recipe], settings: Settings):
    """
    The view recipes menu option: select a recipe to view it.
    """
    
    # Display Current Settings

    print(settings.generate_filter_settings_output(NO_MAX_PREP_TIME))

    # Edit sort/filter settings

    choice = input("Would you like to change these sorting/filtering settings? [Y/N]")

    if choice.upper() == "Y":
        edit_sort_and_filter_settings()

    compare_functions = {
        SortBys.NAME : lambda left, right: compare_attribute(left, right, f'{Recipe._name=}'.split('=')[0]),
        SortBys.PREP_TIME : lambda left, right: compare_attribute(left, right, f'{Recipe._prep_time=}'.split('=')[0])
    }

    # Sort and filter

    check_recipe_satisfies_filters = lambda recipe: check_satisfies_filters(recipe)
    filtered_recipes = filter_recipes(recipes, check_recipe_satisfies_filters)
    filtered_recipes = sort_recipes(filtered_recipes, compare_functions[settings.sort_by])
    
    # Display
    
    while recipe_to_display != -1:

        # User can select which recipe they'd like to view the details of.

        recipe_to_display = display_selection_menu([recipe.format_title() for recipe in filtered_recipes])
        if recipe_to_display == -1:
            break

        # Display details of chosen recipe.

        print(filtered_recipes[recipe_to_display])

        input("Enter any key to exit: ")