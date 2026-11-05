from bs4 import BeautifulSoup, Tag

from parsers.base import RestaurantParser

VEGAN_TAB_TITLE = "VEGÁN MENU"


def _find_tab_pane(section: Tag, tab_title: str, fallback_id: str) -> Tag | None:
    """Locate a Bootstrap tab pane inside `#denne-menu` by its tab label or fallback ID."""
    for link in section.select("ul.recipe_menu a.nav-link"):
        title_el = link.select_one(".title") or link
        title_text = " ".join(title_el.get_text().split()).upper()
        if title_text == tab_title.upper():
            target = str(link.get("data-bs-target") or link.get("href") or "").lstrip(
                "#"
            )
            if target:
                pane = section.find(id=target)
                if isinstance(pane, Tag):
                    return pane

    pane = section.find(id=fallback_id)
    return pane if isinstance(pane, Tag) else None


def _extract_allergens(item: Tag) -> str:
    """Extract comma-separated allergen numbers from `.ri_text span` (e.g. '1,3,9')."""
    for span in item.select(".ri_text span"):
        text = " ".join(span.get_text().split())
        if "alerg" in text.lower() and ":" in text:
            raw_codes = text.split(":", 1)[1]
            codes = [code.strip() for code in raw_codes.split(",") if code.strip()]
            return ",".join(codes)
    return ""


def _parse_recipe_item(item: Tag) -> str | None:
    """Format a single `.recipe_item` block into '<dish> (<allergens>) <price>'."""
    title_el = item.select_one(".ri_text h3") or item.find("h3")
    if title_el is None:
        return None

    name = " ".join(title_el.get_text().split())
    if not name:
        return None

    allergens = _extract_allergens(item)

    price_el = item.select_one(".ri_cart .price") or item.select_one(".price")
    price = " ".join(price_el.get_text().split()) if price_el else ""

    parts = [name]
    if allergens:
        parts.append(f"({allergens})")
    if price:
        parts.append(price)
    return " ".join(parts)


def _parse_pane_items(pane: Tag | None) -> list[str]:
    if pane is None:
        return []
    lines: list[str] = []
    for item in pane.select("div.recipe_item"):
        parsed = _parse_recipe_item(item)
        if parsed:
            lines.append(parsed)
    return lines


class FoodGardenParser(RestaurantParser):
    """Daily menu parser for Food Garden."""

    def parse(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        section = soup.find(id="denne-menu")
        if not isinstance(section, Tag):
            raise ValueError("Could not find '#denne-menu' section in page HTML.")  # noqa: TRY004

        regular_pane = _find_tab_pane(section, "DENNÉ MENU", fallback_id="tab-021")
        vegan_pane = _find_tab_pane(section, VEGAN_TAB_TITLE, fallback_id="tab-031")

        regular_items = _parse_pane_items(regular_pane)
        vegan_items = _parse_pane_items(vegan_pane)

        menu_lines: list[str] = list(regular_items)
        if vegan_items:
            menu_lines.append("VEGÁN MENU:")
            menu_lines.extend(vegan_items)

        return menu_lines


def parse_food_garden_menu(html: str) -> list[str]:
    """Parse raw Food Garden HTML into a list of menu lines."""
    return FoodGardenParser().parse(html)
