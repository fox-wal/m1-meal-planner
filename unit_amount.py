from unit import Unit

DEFAULT_AMOUNT = 1
NO_UNIT = Unit("no unit", "x")

class UnitAmount:
    _unit: Unit
    _amount: float

    def __init__(self, unit: Unit = NO_UNIT, amount: float = DEFAULT_AMOUNT) -> None:
        self._unit = unit
        self._amount = amount

    def get_unit(self) -> Unit:
        return self._unit
    
    def get_amount(self) -> float:
        return self._amount