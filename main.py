#
# MEAL PLANNER
#

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

display_menu(MAIN_MENU)
choice = user_selects_item_from_menu(MAIN_MENU.__len__())
if choice == -1:
    print("Exiting...")
else:
    print(f"[{MAIN_MENU[choice]}] selected.")