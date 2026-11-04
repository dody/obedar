import re
from bs4 import BeautifulSoup

from parsers.base import RestaurantParser, fetch_html

DEFAULT_URL = "https://www.lunch-break.sk/menu-apollo"

_PRICE_ONLY_RE = re.compile(r"^\d+[.,]\d+\s*€$")
_IGNORED_LINES = {
    "POLIEVKA JE ZAHRNUTÁ V CENE MENU",
}


def _normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def parse_lunch_break_menu(html: str) -> list[str]:
    """Parse the active daily menu from Lunch Break HTML.

    Returns a list of lines starting with the day title, preserving section headers,
    joining standalone price paragraphs onto the preceding dish line, and skipping
    informational boilerplate like 'POLIEVKA JE ZAHRNUTÁ V CENE MENU'.
    """
    soup = BeautifulSoup(html, "html.parser")
    menu_section = soup.find(id="menu") or soup

    toggle = (
        menu_section.select_one(".et_pb_toggle.et_pb_toggle_open")
        or menu_section.select_one(".et_pb_toggle")
    )
    if toggle is None:
        return []

    lines: list[str] = []

    title_el = toggle.select_one(".et_pb_toggle_title")
    if title_el is not None:
        title_text = _normalize_whitespace(title_el.get_text())
        if title_text:
            lines.append(title_text)

    content_el = toggle.select_one(".et_pb_toggle_content")
    if content_el is None:
        return lines

    for p in content_el.find_all("p"):
        text = _normalize_whitespace(p.get_text())
        if not text or text.upper() in _IGNORED_LINES:
            continue

        if _PRICE_ONLY_RE.match(text) and lines:
            lines[-1] = f"{lines[-1]} {text}"
        else:
            lines.append(text)

    return lines


class LunchBreakParser(RestaurantParser):
    """Menu parser for Lunch Break (https://www.lunch-break.sk/menu-apollo)."""

    def __init__(self, url: str = DEFAULT_URL, section_id: str = "Lunch Break") -> None:
        super().__init__(url=url, section_id=section_id)

    def parse(self, html: str) -> list[str]:
        return parse_lunch_break_menu(html)


def scrape_lunch_break_menu(url: str = DEFAULT_URL) -> list[str]:
    """Fetch and parse the current daily menu from Lunch Break."""
    html = fetch_html(url)
    return parse_lunch_break_menu(html)
