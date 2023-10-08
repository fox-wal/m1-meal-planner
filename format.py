# Format a line of text using a standardised "heading" format.
def format_heading(heading: str):
    return f"\n--- {heading} ---"

# Format the given number of minutes as a string.
# Return: The given number of minutes as a string in the format "{hours} h {minutes} m"
#      OR "{minutes} m" (if the number of minutes does not exceed 60).
def format_time(minutes: int):
    # EXTENSION: can toggle between just minutes or hours and minutes format
    MINUTES_PER_HOUR = 60
    output = ""
    if minutes > MINUTES_PER_HOUR:
        output += f"{minutes // MINUTES_PER_HOUR} h "
    output += f"{minutes % MINUTES_PER_HOUR} m"
    return output

# Capitalize the given name and replace the underscores with spaces.
def format_var_name(name: str) -> str:
    return name.capitalize().replace('_', ' ')

# Format the given error message.
def format_error(error_message: str):
    return "Error: " + error_message
