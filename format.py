def format_heading(heading: str) -> str:
    """Format a line of text to look like a heading."""
    return f"\n--- {heading} ---"

def format_time(minutes: int) -> str:
    """
    Format the given number of minutes as a string.

    Returns:
        The given number of minutes as a string in the format "{hours} h {minutes} m"
         OR "{minutes} m" (if the number of minutes does not exceed 60).
    """
    # EXTENSION: can toggle between just minutes or hours and minutes format
    MINUTES_PER_HOUR = 60
    output = ""
    if minutes > MINUTES_PER_HOUR:
        output += f"{minutes // MINUTES_PER_HOUR} h "
    output += f"{minutes % MINUTES_PER_HOUR} m"
    return output

def format_var_name(name: str) -> str:
    """Capitalize the given `name` and replace the underscores with spaces."""
    return name.capitalize().replace('_', ' ')

def format_error(error_message: str) -> str:
    """Format the given error message."""
    return "Error: " + error_message
