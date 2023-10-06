from unit import unit

DEFAULT_AMOUNT = 1
NO_UNIT = unit("no unit", "x")

class unit_amount:
    _unit: unit
    _amount: float

    def __init__(self, unit: unit = NO_UNIT, amount: float = DEFAULT_AMOUNT) -> None:
        self._unit = unit
        self._amount = amount

    def get_unit(self) -> unit:
        return self._unit
    
    def get_amount(self) -> float:
        return self._amount