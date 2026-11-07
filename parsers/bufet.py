import re
from datetime import date

from bs4 import BeautifulSoup

from parsers.base import ParserError, RestaurantParser

_DAY_HEADER_RE = re.compile(r"^0?(\d{1,2})\.\s*0?(\d{1,2})\.\s*(\d{4})\b")


def _normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def parse_bufet_menu(html: str, target_date: date | None = None) -> list[str]:
    """Parse the daily menu for `target_date` (defaults to today) from Bufet HTML."""
    active_date = target_date or date.today()
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one("#content article.item .content")
    if content is None:
        raise ParserError(
            "Could not find '#content article.item .content' section in page HTML."
        )

    lines: list[str] = []
    collecting = False

    for row in content.find_all("tr"):
        cells = [_normalize_whitespace(td.get_text()) for td in row.find_all("td")]
        if not cells:
            continue

        first_cell = cells[0]
        header_match = _DAY_HEADER_RE.match(first_cell)
        if header_match:
            if collecting:
                break
            day, month, year = (int(part) for part in header_match.groups())
            if (year, month, day) == (
                active_date.year,
                active_date.month,
                active_date.day,
            ):
                collecting = True
                lines.append(first_cell)
            continue

        if not collecting:
            continue

        if not first_cell or first_cell.lower().startswith(
            ("hmotnosť", "na objednávku")
        ):
            break

        price = cells[1] if len(cells) > 1 else ""
        if price:
            lines.append(f"{first_cell} - {price}")
        else:
            lines.append(first_cell)

    return lines


class BufetParser(RestaurantParser):
    """Daily menu parser for Bufet (https://bufet.urbancomp.sk/)."""

    def __init__(
        self,
        url: str = "",
        section_id: str = "",
        target_date: date | None = None,
    ) -> None:
        super().__init__(url=url, section_id=section_id)
        self.target_date = target_date

    def parse(self, html: str) -> list[str]:
        return parse_bufet_menu(html, target_date=self.target_date)
