from enum import Enum
from format import format_heading, format_var_name, format_time

class SortBys(Enum):
    NAME = 0
    PREP_TIME = 1
    # EXTENSION: LAST_OPENED = 2

class FilterConditions(Enum):
    TAGS = 0
    SEARCH = 1
    PREP_TIME = 2

class Settings:
    # TODO: load these from a file
    # Filters
    active_filters: list[FilterConditions]
    all_tags: list[str]
    active_tags = list[str]
    search_terms: list[str]
    max_prep_time: int
    sort_by: SortBys

    # Filter settings
    tag_union: bool
    keyword_search: bool # Search for keywords instead of exact matches
    # NOTE: I'm opting for linear search because this isn't particularly large
    # scale and it allows for better results, which is more important in this program
    # than speed.

    def __init__(self) -> None:
        self.all_tags = []
        self.active_tags = []
        self.search_terms = []
        self.max_prep_time = 0
        self.sort_by = SortBys.NAME

    def __init__(self, search_terms: list[str], max_prep_time: int, sort_by: SortBys,
                 all_tags: list[str], active_tags = list[str]) -> None:
        self.all_tags = all_tags
        self.active_tags = active_tags
        self.search_terms = search_terms
        self.max_prep_time = max_prep_time
        self.sort_by = sort_by
    
    def generate_filter_settings_output(self, no_max_prep_time_message: str) -> str:
        # Sorting condition
        string = "\n" + format_heading("Sorting")
        string += "\nSort by " + format_var_name(self.sort_by) + '.'

        # Filters
        string += "\n" + format_heading("Filters")
        string += "\nSearch term(s): " + ' '.join(self.search_terms)
        string += "\nTags: " + ", ".join(self.active_tags)
        string += "\nMax preparation time: "
        if self.max_prep_time == 0:
            string += no_max_prep_time_message
        else:
            string += format_time(self.max_prep_time)

        return string
    