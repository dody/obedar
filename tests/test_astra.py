import unittest
from pathlib import Path

from parsers.sme import parse_sme_menu

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class AstraParserTests(unittest.TestCase):
    def test_parses_astra_fixture(self) -> None:
        html = (FIXTURES_DIR / "astra_2026_11_04.html").read_text(encoding="utf-8")
        result = parse_sme_menu(html)
        self.assertEqual(
            result,
            [
                "Obedové menu Streda (04.11.2026)",
                "Lúsková na kyslo so zemiakmi (1,7)",
                "1/A Ovocné tvarohové guľky so strúhankou a maslom 8.10 € (1,3,7)",
                "1/B Maslové špagety s cesnakom, parmezán, chilli, olivový olej, petržlenová vňať 8.10 € (1,3,7)",
                "2. Kurací gyros na miešanom šaláte, hranolky alebo varené zemiaky, tzatziki - bezlepkové 8.60 € (7)",
                "3. Pečená krkovička na čiernom pive, dusená červená kapusta, domáca parená knedľa 9.30 € (1,3,7)",
                "4. Zabíjačkový tanier (jaternica, krvavnica), mastené varené zemiaky s vnaťou, kyslá kapusta 10.90 € (1,3,7)",
            ],
        )


if __name__ == "__main__":
    unittest.main()
