import copy
from recipe import Recipe
from format import *
from main import display_selection_menu, display_menu, input_int
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

def add_ingredients(existing_ingredients: list[str], units: list[Unit]) -> tuple[dict[str, UnitAmount], list[str]]:
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

def add_steps() -> list[str]:
    """User adds steps."""
    steps = []
    step_number = 1

    # Repeat until user types "done".
    while True:
        step = input(f"{step_number}: ")

        # Check for invalid inputs.
        if step.__contains__("\n"):
            print(format_error("Contains invalid characters."))
            continue
        elif len(step) == 0:
            print(format_error("Step cannot be empty."))
            continue
        
        # Check if done.
        if step.lower() == "done":
            break
        else:
            steps.append(step)
        
        step_number += 1

def add_tags(existing_tags: list[str]) -> list[str]:
    """User adds tags."""

    selected_tags = []

    # Show existing tags
    display_menu(existing_tags)

    while True:
        # Choose from existing or add new.
        tag = get_input("Enter tag number or type a new tag.\nOnly letters and hyphens allowed.\n", "-0123456789")

        # If they enter a number, check if can be taken from existing.
        if tag.isnumeric():
            if (int(tag) >= 1) and (int(tag) <= len(existing_tags)):
                selected_tags.append(existing_tags[int(tag) - 1])
            else:
                print(format_error("Invalid tag number."))
                continue
        else:
            for i in tag:
                if i.isnumeric():
                    print(format_error("Cannot contain numbers."))
                    continue
            selected_tags.append(tag.lower())
        
        # Choose whether or not to continue.
        choice = display_selection_menu(["Add another", "Finished"])

        if choice == 1:
            break
    
    return selected_tags

def add_edit_recipe(all_recipes: list[Recipe], existing_ingredients: list[str], existing_tags: list[str], units: list[Unit]) -> tuple[list[Recipe], list[str], list[str]]:
    while True:
        choice = display_selection_menu(["Add recipe", "Finish"])
        if choice == 1:
            break

        name = get_input("Recipe name: ", " -'")
        (ingredient_amounts, additional_ingredients) = add_ingredients(existing_ingredients, units)
        steps = add_steps()
        prep_time = input_int("Prep time in minutes: ", 0)
        tags = add_tags(existing_tags)

        all_recipes.append(Recipe(name, ingredient_amounts, steps, prep_time, tags))

    return (all_recipes, existing_ingredients.__add__(additional_ingredients), existing_tags.__add__(tags))