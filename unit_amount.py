from unit import Unit

class UnitAmount:
    _unit: Unit
    _amount: float

    __DEFAULT_AMOUNT = 1
    
    def __init__(self, unit: Unit = Unit.NO_UNIT, amount: float = __DEFAULT_AMOUNT) -> None:
        self._unit = unit
        self._amount = amount

    def get_unit(self) -> Unit:
        return self._unit
    
    def get_amount(self) -> float:
        return self._amount