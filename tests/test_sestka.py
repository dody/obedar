import unittest
from pathlib import Path

from parsers.sestka import parse_sestka_menu

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class SestkaParserTests(unittest.TestCase):
    def test_parses_sestka_fixture(self) -> None:
        html = (FIXTURES_DIR / "sestka_2026_11_04.html").read_text(encoding="utf-8")
        result = parse_sestka_menu(html)
        self.assertEqual(
            result,
            [
                "Obedové menu Streda (04.11.2026)",
                "S",
            ],
        )

    def test_raises_when_denne_menu_wrapper_missing(self) -> None:
        with self.assertRaises(ValueError):
            parse_sestka_menu("")


if __name__ == "__main__":
    unittest.main()
