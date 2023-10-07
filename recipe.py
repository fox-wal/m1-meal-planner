from unit_amount import UnitAmount

class Recipe:
    _name: str
    _ingredients: dict[str, UnitAmount] # Ingredients and their respective amounts
    _steps: list[str]
    _keywords: list[str] # Used when searching and sorting
    _prep_time: int # In minutes
    _tags: list[str]
    
    def __init__(self, name: str, ingredients: dict[str, UnitAmount], steps: list[str],
                 prep_time: int, tags: list[str]):
        self._name = name
        self._ingredients = ingredients
        self._steps = steps
        self._keywords = name.split(' ').sort()
        self._prep_time = prep_time
        self._tags = tags
    
    def get_name(self) -> str:
        return self._name
    
    def get_ingredients(self) -> dict[str, UnitAmount]:
        return self._ingredients
    
    def get_steps(self) -> list[str]:
        return self._steps
    
    def get_keywords(self) -> list[str]:
        return self._keywords
    
    def get_prep_time(self) -> int:
        return self._prep_time
    
    def get_tags(self) -> list[str]:
        return self._tags