import unittest

from parsers.sestka import parse_sestka_menu

SAMPLE_SME_HTML = """
<!DOCTYPE html>
<html lang="sk">
<body>
<div class="denne_menu left_panel_wrapper">
    <div class="poznamka_k_menu light">
        <p>Otváracie hodiny 11:00 - 21:00 hod.</p>
    </div>
    <div>
        <div class="dnesne_menu">
            <h2>
                Obedové menu
                Pondelok
                (02.11.2026)
            </h2>
            <div class="jedlo_polozka">
                <div class="left">
                    0,33l\t(1,3)\t\tZeleninová na paprike s mrveničkou\t
                </div>
            </div>
            <div class="delimiter"></div>
            <div class="jedlo_polozka">
                <div class="left">
                    130g\t(1,3,7)\t1.\tVyprážané kuracie nugetky, hranolky alebo varené zemiaky, domáca tatárska omáčka\t
                </div>
                <span class="right"><b>8.10 €</b></span>
            </div>
            <div class="delimiter"></div>
            <div class="jedlo_polozka">
                <div class="left">
                    140g\t(7)\t2.\tGrilovaná kuracia sekaná, zemiaková kaša, kyslá uhorka\t
                </div>
                <span class="right"><b>8.60 €</b></span>
            </div>
            <div class="delimiter"></div>
            <div class="jedlo_polozka">
                <div class="left">
                    130g\t(7)\t3.\tTrhané bravčové &quot;pulled pork&quot; na hranolkách s cheddarovou omáčkou, nakladané cibuľky - bezlepkové\t
                </div>
                <span class="right"><b>9.30 €</b></span>
            </div>
            <div class="delimiter"></div>
            <div class="jedlo_polozka">
                <div class="left">
                    450g+\t(1,3,7)\t4.\tZabíjačkový tanier (jaternica, krvavnica), mastené varené zemiaky s vnaťou, kyslá kapusta\t
                </div>
                <span class="right"><b>10.90 €</b></span>
            </div>
            <div class="delimiter"></div>
        </div>
    </div>
    <div>
        <div class="ostatne_menu hidden">
            <h2>Obedové menu Utorok (03.11.2026)</h2>
            <div class="jedlo_polozka">
                <div class="left">0,33l\t(1)\t\tKelová s párkom\t</div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""


class SestkaParserTests(unittest.TestCase):
    def test_parses_today_menu_in_requested_format_and_ignores_other_days(self) -> None:
        result = parse_sestka_menu(SAMPLE_SME_HTML)
        self.assertEqual(
            result,
            [
                "Obedové menu Pondelok (02.11.2026)",
                "Zeleninová na paprike s mrveničkou (1,3)",
                "1. Vyprážané kuracie nugetky, hranolky alebo varené zemiaky, domáca tatárska omáčka 8.10 € (1,3,7)",
                "2. Grilovaná kuracia sekaná, zemiaková kaša, kyslá uhorka 8.60 € (7)",
                '3. Trhané bravčové "pulled pork" na hranolkách s cheddarovou omáčkou, nakladané cibuľky - bezlepkové 9.30 € (7)',
                "4. Zabíjačkový tanier (jaternica, krvavnica), mastené varené zemiaky s vnaťou, kyslá kapusta 10.90 € (1,3,7)",
            ],
        )

    def test_returns_empty_list_when_no_today_menu_present(self) -> None:
        html = '<div class="denne_menu"><div class="ostatne_menu hidden"></div></div>'
        self.assertEqual(parse_sestka_menu(html), [])

    def test_raises_when_denne_menu_wrapper_missing(self) -> None:
        with self.assertRaises(ValueError):
            parse_sestka_menu("<html><body><h1>Request Blocked</h1></body></html>")


if __name__ == "__main__":
    unittest.main()
