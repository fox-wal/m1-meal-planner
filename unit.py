from unit import Unit

class Unit:
    _name: str
    _symbol: str 

    def __init__(self, name: str, symbol: str):
        self._name = name
        self._symbol = symbol
    
    def get_name(self) -> str:
        return self._name
    
    def get_symbol(self) -> str:
        return self._symbol