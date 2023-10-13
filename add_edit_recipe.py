import copy
from recipe import Recipe
from format import *
from main import display_selection_menu
from unit_amount import *

def get_input(prompt: str, allowed_symbols: str = " ") -> str:
    """
    Prompt the user for an input until they enter a valid one.

    Args:
        prompt: The prompt to display to the user each time before they enter an input.
        allowed_symbols: Valid non-alphabetic characters.
    
    Returns:
        Valid alphabetic (except for the `allowed_symbols`) user input.
    """
    
    while True:
        # Get input
        user_input = input(prompt)

        # Will skip this if fully alphabetic
        if not user_input.isalpha():
            # Check each character.
            for i in user_input:
                if not (i.isalpha() or user_input.__contains__(i)):
                    print(format_error(f"Character '{i}' not allowed."))
                    # Prompt for input again if invalid character is detected.
                    continue

        return user_input

def get_amount(prompt: str) -> float:
    """
    Display the `prompt` and suitable error messages to the user until they enter a valid float > 0.
    """
    while True:
        try:
            amount = float(input(prompt))
            if amount > 0:
                return amount
            else:
                print(format_error("Must be greater than 0."))
        except ValueError:
            print(format_error("Must be a real number."))

def add_ingredient(existing_ingredients: list[str]) -> str | None:
    """
    Allows the user to enter an ingredient either by selecting it from `existing_ingredients`, adding a new ingredient, or entering a one-off ingredient.

    Returns:
        The ingredient, if entered.
        None if no ingredient entered.

        True if a new ingredient was added.
        False otherwise
    """
    ALLOWED_SYMBOLS = " -'"

    # Select, add new, or add one-off
    print("How would you like to add an ingredient?")
    method = display_selection_menu(["Select from existing", "Add new", "Add one-off"])

    # Select: display existing --> user selects one or exits back to above menu.
    if method == 0:
        print("Select an ingredient:")
        selection = display_selection_menu(existing_ingredients)
        if selection is None:
            return None
        else:
            return existing_ingredients[selection]

    # Add new/one-off: type in new ingredient. Leave blank to cancel.
    else:
        if method == 1:
            prompt = "Enter new ingredient: "
        else:
            prompt = "Enter one-off ingredient: "

        ingredient += get_input(prompt, ALLOWED_SYMBOLS)

        if len(ingredient) == 0:
            return None
        else:
            if method == 1:
                ingredient = "*" + ingredient
            return ingredient

def add_ingredients(existing_ingredients: list[str], units: list[Unit]) -> (dict[str, UnitAmount], list[str]):
    """
    User adds ingredients and corresponding amounts.

    Returns:
        The ingredients and corresponding amounts that the user entered.

        The (possibly) updated version of the `existing_ingredients` list.
    """

    ingredients_and_amounts: dict[str, UnitAmount] = {}

    ingredient_list_finished = False

    # Loop until all ingredients added.
    while not ingredient_list_finished:

        ingredient: str = None
        unit_amount: UnitAmount = None

        # Loop until ingredient confirmed or canceled.
        while ingredient is None:
            ingredient = add_ingredient(existing_ingredients)

            if ingredient is None:
                continue
            if ingredient[0] == "*":
                ingredient = ingredient[1:]
                existing_ingredients.append(ingredient)

        # Enter amount.
        amount = get_amount()

        # Select unit.
        unit_menu = [f"{unit_name} ({unit_symbol})" for unit_name, unit_symbol in units.items()]
        unit_index = display_selection_menu(unit_menu)
        unit_amount = UnitAmount(units[unit_menu[unit_index].split()[0]], amount)

        # Confirm or cancel.
        ingredient_confirmed = bool(1 - display_selection_menu([f"Save ingredient entry <{unit_amount.as_string()} {ingredient}>", "Cancel"]))

        # Add to dictionary.
        if ingredient_confirmed:
            ingredients_and_amounts[ingredient.lower()] = copy.deepcopy(unit_amount)
            print("Ingredient added to recipe.")

        # Select whether to add ingredient or finish
        ingredient_list_finished = bool(display_selection_menu(["Add ingredient", "Finish"]))
        if ingredient_list_finished:
            break
    
    return (ingredients_and_amounts, existing_ingredients)

def add_edit_recipe(all_recipes: list[Recipe]) -> list[Recipe]:
    """
    - [-] 1. Add ingredients
        - [-] 1. Select from existing ingredients
        - [-] 2. or add new
        - [-] 3. or type custom (one-off)
    - [-] 2. ...and amounts
        - [-] 1. Enter amount
        - [-] 2. Select from existing units
    - [ ] 3. Add steps
        - [ ] 1. Add individually
        - [ ] 2. _State duration for each one_
    - [ ] 4. Add tags
    """
