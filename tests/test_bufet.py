import unittest
from datetime import date
from pathlib import Path

from parsers.bufet import BufetParser, parse_bufet_menu

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class BufetParserTests(unittest.TestCase):
    def test_parses_bufet_fixture_for_wednesday(self) -> None:
        html = (FIXTURES_DIR / "bufet_2026_11_07.html").read_text(encoding="utf-8")
        target_date = date(2026, 11, 4)
        expected = [
            "4.11.2026 Streda",
            "Kuracie soté, placka, ryža - 1;3 - 7,30€",
            "Bravčová cigánska pečienka, zemiakové pyré, uhorky - 7 - 7,30€",
            "Šúľance plnené makom a lekvárom, tvaroh ,mak - 7,30€",
        ]
        self.assertEqual(parse_bufet_menu(html, target_date=target_date), expected)
        self.assertEqual(BufetParser(target_date=target_date).parse(html), expected)


if __name__ == "__main__":
    unittest.main()
