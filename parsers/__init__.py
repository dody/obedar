from parsers.base import RestaurantParser
from parsers.pressburg import PressburgParser, get_pressburg_menu, parse_pressburg_menu

RESTAURANTS: list[RestaurantParser] = [
    PressburgParser(),
]

__all__ = [
    "RESTAURANTS",
    "RestaurantParser",
    "PressburgParser",
    "get_pressburg_menu",
    "parse_pressburg_menu",
]

