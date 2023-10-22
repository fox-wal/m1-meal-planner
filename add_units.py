from format import format_heading

def add_units(units: list[Unit], conversions: dict[str, dict[str, int]]):
    print(format_heading("Add New Unit"))
    name = input("Name:")
    if not name.isalpha():
        raise ValueError("Unit name must only contain alphabetic characters.")
    symbol = input("Symbol:")
    if len(symbol) > MAX_SYMBOL_LEN:
        raise ValueError("Symbol cannot exceed {} characters in length.".format(MAX_SYMBOL_LENGTH))
    elif not symbol.isalpha():
        raise ValueError("Symbol must only contain alphabetic characters.")

    unit_names = [unit.get_name() for unit in units]
    unit_symbols = [unit.get_symbol() for unit in units]

    if unit_names.__contains__(name):
        raise ValueError("Unit already exists. *Would you like to edit it?*")
    if unit_symbols.__contains__(symbol):
        raise ValueError("Symbol already exists. *Please enter a different one?*")
    print("Does this unit go below any other in the hierarchy? (e.g. millilitres goes below litres)")
    in_hierarchy = bool(1 - display_selection_menu(["yes", "no"]))
    if in_hierarchy:
        print("Which unit does \"{}\" go into?".format(name))
        higher_unit = units[display_selection_menu(units)] # TODO: format units properly
        amount = float(input("How many {} are there in a {}?".format(name, higher_unit.get_name())))
        conversions[higher_unit.get_name()][name] = amount
    units.append(Unit(name, symbol))