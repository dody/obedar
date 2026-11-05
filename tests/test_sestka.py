import unittest
from pathlib import Path

from parsers.sestka import parse_sestka_menu

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class SestkaParserTests(unittest.TestCase):
    def test_parses_sestka_2026_11_05_fixture(self) -> None:
        html = (FIXTURES_DIR / "sestka_2026_11_05.html").read_text(encoding="utf-8")
        result = parse_sestka_menu(html)
        self.assertEqual(
            result,
            [
                "Obedové menu Štvrtok (05.11.2026)",
                "Boršč s kyslou smotanou 7 2.50 €",
                "Zemiaková na kyslo 1,7 2.50 €",
                "1. Kur. prsia s mladým listovým špenátom, oštiepkom,šunkou a volským okom, 1/2 ryža, 1/2 peč.zemiaky 3,7 8.00 €",
                "2. Vypr.bravč. kapsa pln.slaninkou, údeným syrom a mladou cibuľkou, 1/2 ryža, 1/2 peč.zemiaky, tat.omáčka 1,3,7,10 8.00 €",
                "3. Tradičný Segedínsky guláš s kyslou smotanou, knedľa 1,3,7 8.00 €",
                "4. Cena menu s polievkou 8,50 € 8.50 €",
            ],
        )

    def test_raises_when_denne_menu_wrapper_missing(self) -> None:
        with self.assertRaises(ValueError):
            parse_sestka_menu("")


if __name__ == "__main__":
    unittest.main()
