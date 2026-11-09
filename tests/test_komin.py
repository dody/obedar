import unittest
from pathlib import Path

from parsers.base import ParserError
from parsers.komin import parse_komin_menu

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class KominParserTests(unittest.TestCase):
    def test_parses_komin_fixture(self) -> None:
        html = (FIXTURES_DIR / "komin_2026_11_09.html").read_text(encoding="utf-8")
        result = parse_komin_menu(html)
        self.assertEqual(
            result,
            [
                "Obedové menu Pondelok (09.11.2026)",
                "Šošovicová na kyslo (1,7)",
                "1: 350g Hovädzí perkelt, maslové halušky, kyslá smotana (1,3,7)",
                "2: 150g/160g Kuracia rolka plnená bazalkovým pestom a parmezánom, tagliatelle, paradajková omáčka (7)",
                "3: 150g/200g Bravčový černohorský rezeň, zemiaková kaša, mozzarella, cesnakový dip (1,3,7)",
            ],
        )

    def test_raises_when_denne_menu_wrapper_missing(self) -> None:
        with self.assertRaises(ParserError):
            parse_komin_menu("")


if __name__ == "__main__":
    unittest.main()
