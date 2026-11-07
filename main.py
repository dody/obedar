import json
import os
import socket
import sys
import time
from pathlib import Path
from typing import Any

import requests

from parsers.base import ParserError
from restaurants import RESTAURANTS, RestaurantConfig

ENV_PATH = Path(__file__).resolve().parent / ".env"


def _load_api_url(env_path: Path = ENV_PATH) -> str | None:
    """Load API_URL from environment variables or a local .env file if present."""
    if env_url := os.environ.get("API_URL"):
        return env_url.strip()

    if not env_path.is_file():
        return None

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == "API_URL":
            return value.strip().strip("\"'")

    return None


def build_menu_data(
    restaurants: list[RestaurantConfig] = RESTAURANTS,
    author: str = socket.gethostname(),
    timeout: float = 15.0,
) -> dict[str, Any]:
    """Scrape all configured restaurants and return the payload dict ready for JSON upload."""
    sections: list[dict[str, Any]] = []
    for entry in restaurants:
        parser = entry.parser(url=entry.url, section_id=entry.section_id)
        try:
            menu_lines = parser.get_menu(timeout=timeout)
        except ParserError as exc:
            menu_lines = [
                entry.url,
                f"PARSER ERROR: {exc}",
            ]
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


def push_to_google_sheets(data: dict[str, Any], url: str) -> None:
    time_start = time.time()
    response = requests.post(url, json=data)
    print(response.json())
    print("Time taken:", time.time() - time_start, "seconds")


def main() -> dict[str, Any]:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    data = build_menu_data()
    print(json.dumps(data, ensure_ascii=False, indent=2))

    api_url = _load_api_url()
    if api_url:
        push_to_google_sheets(data, api_url)

    return data


if __name__ == "__main__":
    main()
