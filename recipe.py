from unit_amount import Unit_amount

class Recipe:
    _name: str
    _ingredients: dict[str, Unit_amount] # Ingredients and their respective amounts
    _steps: list[str]
    _keywords: list[str] # Used when searching and sorting
    _duration: int # Duration in minutes
    _tags: list[str]
    
    def __init__(self, name: str, ingredients: dict[str, Unit_amount], steps: list[str],
                 duration: int, tags: list[str]):
        self._name = name
        self._ingredients = ingredients
        self._steps = steps
        self._keywords = name.split(' ').sort()
        self._duration = duration
        self._tags = tags
    
    def get_name(self) -> str:
        return self._name
    
    def get_ingredients(self) -> dict[str, Unit_amount]:
        return self._ingredients
    
    def get_steps(self) -> list[str]:
        return self._steps
    
    def get_keywords(self) -> list[str]:
        return self._keywords
    
    def get_prep_time(self) -> int:
        return self._duration
    
    def get_tags(self) -> list[str]:
        return self._tags