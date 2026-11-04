import re

from bs4 import BeautifulSoup, Tag

from parsers.base import RestaurantParser

_UNIT_AMOUNT = r"\d+(?:[.,]\d+)?\s*(?:g|kg|ml|l|dl|cl)\+?"
_WEIGHT_EXPR = rf"{_UNIT_AMOUNT}(?:\s*/\s*{_UNIT_AMOUNT})*"

_WEIGHT_ONLY_RE = re.compile(rf"^{_WEIGHT_EXPR}$", re.IGNORECASE)
_LEADING_WEIGHT_RE = re.compile(rf"^{_WEIGHT_EXPR}\s+", re.IGNORECASE)
_TRAILING_WEIGHT_RE = re.compile(rf"\s+{_WEIGHT_EXPR}$", re.IGNORECASE)

_PAREN_GROUP_RE = re.compile(r"^\(\s*(.*?)\s*\)$")
_ALLERGEN_INNER_RE = re.compile(
    r"^(?:alerg[eé]ny\s*:\s*)?(?:\d{1,2}(?:\s*[,/]\s*\d{1,2})*|ø)$",
    re.IGNORECASE,
)
_LEADING_ALLERGEN_RE = re.compile(
    r"^\(\s*((?:alerg[eé]ny\s*:\s*)?(?:\d{1,2}(?:\s*[,/]\s*\d{1,2})*|ø)?)\s*\)\s*",
    re.IGNORECASE,
)
_TRAILING_ALLERGEN_RE = re.compile(
    r"\s*\(\s*((?:alerg[eé]ny\s*:\s*)?(?:\d{1,2}(?:\s*[,/]\s*\d{1,2})*|ø)?)\s*\)$",
    re.IGNORECASE,
)
_TRAILING_PRICE_RE = re.compile(r"\s+(\d+(?:[.,]\d+)?\s*€)$")


def _normalize_allergen_inner(inner: str) -> str:
    cleaned = re.sub(r"^alerg[eé]ny\s*:\s*", "", inner.strip(), flags=re.IGNORECASE)
    if not cleaned:
        return ""
    cleaned = re.sub(r"\s*([,/])\s*", r"\1", cleaned)
    cleaned = " ".join(cleaned.split())
    return f"({cleaned})"


def _normalize_allergen_group(group: str) -> str:
    match = _PAREN_GROUP_RE.match(group.strip())
    if not match:
        return ""
    return _normalize_allergen_inner(match.group(1))


def _is_structured_sme_columns(cols: list[str]) -> bool:
    if len(cols) not in (4, 5):
        return False
    weight_col, allergen_col, number_col, dish_col = cols[:4]
    if not dish_col:
        return False
    if weight_col and not _WEIGHT_ONLY_RE.match(weight_col):
        return False
    if allergen_col:
        match = _PAREN_GROUP_RE.match(allergen_col)
        if not match:
            return False
        inner = match.group(1).strip()
        if inner and not _ALLERGEN_INNER_RE.match(inner):
            return False
    if len(number_col) > 8:
        return False
    return not (len(cols) == 5 and "€" not in cols[4])


def _format_line(dish: str, price: str, allergens: str) -> str:
    parts = [dish]
    if price:
        parts.append(price)
    if allergens:
        parts.append(allergens)
    return " ".join(part for part in parts if part)


def _parse_freeform_item(raw_text: str, right_price: str) -> str | None:
    text = " ".join(raw_text.split())
    if not text:
        return None

    price = right_price
    if not price:
        price_match = _TRAILING_PRICE_RE.search(text)
        if price_match:
            price = " ".join(price_match.group(1).split())
            text = text[: price_match.start()].strip()

    text = _LEADING_WEIGHT_RE.sub("", text).strip()

    allergens = ""
    lead_alg = _LEADING_ALLERGEN_RE.match(text)
    if lead_alg:
        allergens = _normalize_allergen_inner(lead_alg.group(1))
        text = text[lead_alg.end():].strip()
    else:
        trail_alg = _TRAILING_ALLERGEN_RE.search(text)
        if trail_alg:
            allergens = _normalize_allergen_inner(trail_alg.group(1))
            text = text[: trail_alg.start()].strip()

    text = _TRAILING_WEIGHT_RE.sub("", text).strip()
    if not text:
        return None

    return _format_line(text, price, allergens)


def _parse_menu_item(item: Tag) -> str | None:
    """Format a single `div.jedlo_polozka` row into '<dish> [<price>] [(<allergens>)]'."""
    left_el = item.select_one(".left")
    if left_el is None:
        return None

    right_el = item.select_one(".right")
    right_price = " ".join(right_el.get_text().split()) if right_el else ""

    raw_left = left_el.get_text().strip(" \r\n")
    if "\t" in raw_left:
        cols = [" ".join(col.split()) for col in raw_left.split("\t")]
        while len(cols) > 4 and not cols[-1]:
            cols.pop()
        if _is_structured_sme_columns(cols):
            allergens = _normalize_allergen_group(cols[1]) if cols[1] else ""
            number = cols[2]
            dish_name = cols[3]
            dish = f"{number} {dish_name}" if number else dish_name
            price = right_price or (cols[4] if len(cols) == 5 else "")
            return _format_line(dish, price, allergens)

    return _parse_freeform_item(raw_left, right_price)


class SmeParser(RestaurantParser):
    """Daily menu parser for restaurants hosted on restauracie.sme.sk."""

    def parse(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        menu_wrapper = soup.select_one("div.denne_menu")
        if not isinstance(menu_wrapper, Tag):
            raise ValueError("Could not find 'div.denne_menu' section in page HTML.")  # noqa: TRY004

        menu_lines: list[str] = []
        for today_block in menu_wrapper.select("div.dnesne_menu"):
            item_lines: list[str] = []
            for item in today_block.select("div.jedlo_polozka"):
                parsed = _parse_menu_item(item)
                if parsed:
                    item_lines.append(parsed)

            if item_lines:
                heading_el = today_block.find("h2")
                if isinstance(heading_el, Tag):
                    heading_text = " ".join(heading_el.get_text().split())
                    if heading_text:
                        menu_lines.append(heading_text)
                menu_lines.extend(item_lines)

        return menu_lines


def parse_sme_menu(html: str) -> list[str]:
    """Parse raw restauracie.sme.sk HTML into a list of formatted menu lines."""
    return SmeParser().parse(html)
