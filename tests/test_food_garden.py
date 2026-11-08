import unittest
from pathlib import Path

from main import build_menu_data
from parsers.food_garden import FoodGardenParser, parse_food_garden_menu
from restaurants import RestaurantConfig

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"

EXPECTED_FOOD_GARDEN_MENU = [
    "Hovädzia polievka s mäsom a cestovinou (1,3,9) 1 €",
    "Karfiolová polievka s mrkvou a hráškom (1) 1 €",
    "Kurací steak, chedarová omáčka, varené zemiaky (1,7) 8.40 €",
    "Bowl kura (kuracie kúsky, jazmínová ryža, zelenina, edamame, mango, sezam, dresing) (6,11) 8.90 €",
    "Restovaná kuracia pečienka na slaninke, dusená ryža, kyslá uhorka (1,12) 8.40 €",
    "Vyprážané mini rezne z bravčovej panenky, americké zemiaky, dresing (1,3,7) 8.90 €",
    "Lasagne so šampiňónmi, syrom a paradajkovou salsou (1,3,7) 8.40 €",
    "Bravčová panenka v slaninke, hríbová omáčka,opekané baby zemiaky (1,7) 8.90 €",
    "VEGÁN MENU:",
    "Šošovicová polievka so zeleninou (6) 1 €",
    "Vyprážaný syr v panko strúhanke, varené baby zemiaky, americký dresing (1,6) 8.40 €",
    "Tempeh kocky na hubovej omáčke, basmati ryža (6) 8.40 €",
    "Domáce lečo s tofu a sójovým párkom, varené zemiaky (6) 8.40 €",
    "Bowl falafel (jazmínová ryža, zelenina, edamame, mango, sezam, dresing) (6,11) 8.90 €",
]


class _StubFoodGardenParser(FoodGardenParser):
    def fetch_html(self, timeout: float = 15.0) -> str:
        return (FIXTURES_DIR / "food_garden_2026_11_04.html").read_text(
            encoding="utf-8"
        )


class _FailingParser(FoodGardenParser):
    def fetch_html(self, timeout: float = 15.0) -> str:
        return ""


class _EmptyMenuParser(FoodGardenParser):
    def fetch_html(self, timeout: float = 15.0) -> str:
        return "<div id='denne-menu'></div>"


class FoodGardenParserTests(unittest.TestCase):
    def test_parses_food_garden_fixture(self) -> None:
        html = (FIXTURES_DIR / "food_garden_2026_11_04.html").read_text(
            encoding="utf-8"
        )
        result = parse_food_garden_menu(html)
        self.assertEqual(result, EXPECTED_FOOD_GARDEN_MENU)

    def test_build_menu_data_produces_expected_payload_structure(self) -> None:
        configs = [
            RestaurantConfig(
                section_id="Food Garden",
                url="https://pressburg.foodgarden.sk/#denne-menu",
                parser=_StubFoodGardenParser,
            )
        ]
        data = build_menu_data(restaurants=configs, author="python script 1")
        self.assertEqual(
            data,
            {
                "author": "python script 1",
                "sections": [
                    {
                        "section_id": "Food Garden",
                        "menu": EXPECTED_FOOD_GARDEN_MENU,
                    }
                ],
            },
        )

    def test_build_menu_data_includes_error_lines_when_parser_fails(self) -> None:
        configs = [
            RestaurantConfig(
                section_id="Food Garden",
                url="https://pressburg.foodgarden.sk/#denne-menu",
                parser=_FailingParser,
            )
        ]
        data = build_menu_data(restaurants=configs, author="python script 1")
        self.assertEqual(
            data,
            {
                "author": "python script 1",
                "sections": [
                    {
                        "section_id": "Food Garden",
                        "menu": [
                            "https://pressburg.foodgarden.sk/#denne-menu",
                            "PARSER ERROR: Could not find '#denne-menu' section in page HTML.",
                        ],
                    }
                ],
            },
        )

    def test_build_menu_data_includes_error_lines_when_menu_is_empty(self) -> None:
        configs = [
            RestaurantConfig(
                section_id="Bufet",
                url="https://bufet.urbancomp.sk/",
                parser=_EmptyMenuParser,
            )
        ]
        data = build_menu_data(restaurants=configs, author="python script 1")
        self.assertEqual(
            data,
            {
                "author": "python script 1",
                "sections": [
                    {
                        "section_id": "Bufet",
                        "menu": [
                            "https://bufet.urbancomp.sk/",
                            "PARSER ERROR: No menu items found.",
                        ],
                    }
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
