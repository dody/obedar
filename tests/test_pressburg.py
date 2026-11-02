import unittest

from parsers.pressburg import parse_pressburg_menu

SAMPLE_HTML = """
<!doctype html>
<html lang="sk">
<body>
<section class="recipe_menu_area" id="denne-menu">
    <ul class="nav nav-tabs recipe_menu" id="myTab-2" role="tablist">
        <li class="nav-item">
            <a href="#" class="nav-link active" data-bs-target="#tab-021">
                <span class="title">DENNÉ MENU</span>
            </a>
        </li>
        <li class="nav-item">
            <a href="#" class="nav-link" data-bs-target="#tab-031">
                <span class="title">VEGÁN MENU</span>
            </a>
        </li>
    </ul>
    <div class="tab-content" id="myTabContent">
        <div class="tab-pane fade show active" id="tab-021">
            <div class="recipe_item">
                <div class="ri_content">
                    <div class="ri_text">
                        <h3>Zeleninový vývar s cestovinou</h3>
                        <span>Objem: 0,33l</span>
                        <span> ｜ Alergény : 1,3,9</span>
                    </div>
                    <div class="ri_cart">
                        <h5 class="price"><span><bdi>1&nbsp;<span>&euro;</span></bdi></span></h5>
                    </div>
                </div>
            </div>
            <div class="recipe_item">
                <div class="ri_content">
                    <div class="ri_text">
                        <h3>Bravčová panenka v slaninke, hríbová omáčka,opekané baby zemiaky</h3>
                        <span>Hmotnosť: 150g</span>
                        <span> ｜ Alergény : 1,7</span>
                    </div>
                    <div class="ri_cart">
                        <h5 class="price"><span><bdi>8.90&nbsp;<span>&euro;</span></bdi></span></h5>
                    </div>
                </div>
            </div>
        </div>
        <div class="tab-pane fade" id="tab-031">
            <div class="recipe_item">
                <div class="ri_content">
                    <div class="ri_text">
                        <h3>Pórová krémová polievka</h3>
                        <span>Objem: 0,33l</span>
                        <span> ｜ Alergény : 1,9</span>
                    </div>
                    <div class="ri_cart">
                        <h5 class="price"><span><bdi>1&nbsp;<span>&euro;</span></bdi></span></h5>
                    </div>
                </div>
            </div>
            <div class="recipe_item">
                <div class="ri_content">
                    <div class="ri_text">
                        <h3>Brokolicový krém</h3>
                        <span>Objem: 0,33l</span>
                    </div>
                    <div class="ri_cart">
                        <h5 class="price"><span><bdi>1&nbsp;<span>&euro;</span></bdi></span></h5>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
</body>
</html>
"""


class PressburgParserTests(unittest.TestCase):
    def test_parses_regular_and_vegan_menus_into_single_list(self) -> None:
        result = parse_pressburg_menu(SAMPLE_HTML)
        self.assertEqual(
            result,
            [
                "Zeleninový vývar s cestovinou (1,3,9) 1 €",
                "Bravčová panenka v slaninke, hríbová omáčka,opekané baby zemiaky (1,7) 8.90 €",
                "VEGÁN MENU",
                "Pórová krémová polievka (1,9) 1 €",
                "Brokolicový krém 1 €",
            ],
        )


if __name__ == "__main__":
    unittest.main()

