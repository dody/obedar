import json
import sys
from typing import Any

from restaurants import AUTHOR, RESTAURANTS, RestaurantConfig


def build_menu_data(
    restaurants: list[RestaurantConfig] = RESTAURANTS,
    author: str = AUTHOR,
    timeout: float = 15.0,
) -> dict[str, Any]:
    """Scrape all configured restaurants and return the payload dict ready for JSON upload."""
    sections: list[dict[str, Any]] = []
    for entry in restaurants:
        parser = entry.parser(url=entry.url, section_id=entry.section_id)
        menu_lines = parser.get_menu(timeout=timeout)
        sections.append(
            {
                "section_id": entry.section_id,
                "menu": menu_lines,
            }
        )

    return {
        "author": author,
        "sections": sections,
    }


def main() -> dict[str, Any]:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    data = build_menu_data()
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return data


if __name__ == "__main__":
    main()
