from dataclasses import dataclass

from parsers.base import RestaurantParser
from parsers.pressburg import PressburgParser


@dataclass(frozen=True)
class RestaurantConfig:
    """Configuration mapping a restaurant section ID and URL to its parser class."""

    section_id: str
    url: str
    parser: type[RestaurantParser]


AUTHOR = "python script 1"

# Global registry of restaurants to scrape and include in the JSON payload.
RESTAURANTS: list[RestaurantConfig] = [
    RestaurantConfig(
        section_id="Food Garden",
        url="https://pressburg.foodgarden.sk/#denne-menu",
        parser=PressburgParser,
    ),
    # Add future restaurants here, for example:
    # RestaurantConfig(
    #     section_id="Astra",
    #     url="https://...",
    #     parser=AstraParser,
    # ),
    # RestaurantConfig(
    #     section_id="Pizzeria Rotunda",
    #     url="https://...",
    #     parser=RotundaParser,
    # ),
    # RestaurantConfig(
    #     section_id="Šestka",
    #     url="https://...",
    #     parser=SestkaParser,
    # ),
]

