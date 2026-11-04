from pathlib import Path
import unittest

from parsers.lunch_break import LunchBreakParser, parse_lunch_break_menu

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class LunchBreakParserTests(unittest.TestCase):
    def test_parses_lunch_break_fixture(self) -> None:
        html = (FIXTURES_DIR / "lunch_break_2026_11_04.html").read_text(encoding="utf-8")
        result = parse_lunch_break_menu(html)
        expected = [
            "Štvrtok 05.11.2026",
            "POLIEVKA",
            "0,3l Zelerový krém s bylinkovými krutónmi (1,7,9) / Hovädzí vývar s rezancami a bylinkovými haluškami (1,3,9)",
            "MÄSOVÉ MENU",
            "A, 140g/200g Kuracie prsia Formaggio zapečené s brokolicou a mozzarellou, zemiakové gnocchi, omáčka z dvoch druhov syra, šalátik (1,3,7) 9,50 €",
            "B, 140g/200g Medailóniky z panenky v marináde teriyaki, pražená ryža so zeleninou, pak choi a klíčky fazule mungo (2,4,6,11,14) 9,90 €",
            "BEZMÄSITÉ MENU",
            "C, 350g TRIO – vyprážaný syr Gouda, vyprážaný karfiól a šampiňóny, varené zemiaky s petržlenovou vňaťou, naša tatárska omáčka (1,3,7) 9,50 €",
            "ŠPECIÁL MENU",
            "160g/200g Vihorlatské ragú z daniela a srnca so slivkami a borievkami, domáca karlovarská knedľa s tymiánom a petržlenovou vňaťou, hruška nakladaná v červenom víne (1,3,7,12) 12,90 €",
            "ŠPECIÁL POLIEVKA",
            "0,6l Sviatočná kapustnica s bravčovým mäsom,údeným kolenom,mäsovými guľkami, klobásou a lesnými hubami, maďarský kváskový chlieb, kyslá smotana (1,7) – podávané bez dennej polievky (1,7) 8,90 €",
        ]
        self.assertEqual(result, expected)
        self.assertEqual(LunchBreakParser().parse(html), expected)


if __name__ == "__main__":
    unittest.main()
