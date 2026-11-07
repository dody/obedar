from dataclasses import dataclass

from parsers.base import RestaurantParser
from parsers.bufet import BufetParser
from parsers.food_garden import FoodGardenParser
from parsers.lunch_break import LunchBreakParser
from parsers.sestka import SestkaParser
from parsers.sme import SmeParser


@dataclass(frozen=True)
class RestaurantConfig:
    """Configuration mapping a restaurant section ID and URL to its parser class."""

    section_id: str
    url: str
    parser: type[RestaurantParser] | None = None


# Global registry of restaurants to scrape and include in the JSON payload.
RESTAURANTS: list[RestaurantConfig] = [
    RestaurantConfig(
        section_id="Food Garden",
        url="https://pressburg.foodgarden.sk/#denne-menu",
        parser=FoodGardenParser,
    ),
    RestaurantConfig(
        section_id="Astra",
        url="https://restauracie.sme.sk/restauracia/plzenska-astra_153-ruzinov_2980/denne-menu",
        parser=SmeParser,
    ),
    RestaurantConfig(
        section_id="Šestka",
        url="https://restauracie.sme.sk/restauracia/sestka-canteen_10346-ruzinov_2980/denne-menu",
        parser=SestkaParser,
    ),
    RestaurantConfig(
        section_id="Lunch Break",
        url="https://www.lunch-break.sk/menu-apollo",
        parser=LunchBreakParser,
    ),
    RestaurantConfig(
        section_id="Bufet",
        url="https://bufet.urbancomp.sk/",
        parser=BufetParser,
    ),
    # Add future restaurants here, for example:
    # RestaurantConfig(
    #     section_id="Pizzeria Rotunda",
    #     url="https://...",
    #     parser=RotundaParser,
    # ),
]
