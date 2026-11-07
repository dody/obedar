from abc import ABC, abstractmethod
from urllib.parse import urldefrag
from urllib.request import Request, urlopen

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "sk-SK,sk;q=0.9,cs;q=0.8,en-US;q=0.7,en;q=0.6",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}


def fetch_html(url: str, timeout: float = 15.0) -> str:
    """Download raw HTML from `url` and decode it using the response charset (default UTF-8)."""
    clean_url = urldefrag(url).url
    request = Request(clean_url, headers=DEFAULT_HEADERS)
    with urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


class ParserError(Exception):
    """Raised when a restaurant page's HTML structure cannot be parsed."""


class RestaurantParser(ABC):
    """Base interface for restaurant daily menu parsers."""

    def __init__(self, url: str = "", section_id: str = "") -> None:
        self.url = url
        self.section_id = section_id

    def fetch_html(self, timeout: float = 15.0) -> str:
        if not self.url:
            raise ValueError(
                f"{self.__class__.__name__} requires a non-empty URL to fetch HTML."
            )
        return fetch_html(self.url, timeout=timeout)

    @abstractmethod
    def parse(self, html: str) -> list[str]:
        """Parse raw HTML and return the menu as a simple list of lines."""

    def get_menu(self, timeout: float = 15.0) -> list[str]:
        """Fetch the restaurant page and return the parsed list of menu lines."""
        html = self.fetch_html(timeout=timeout)
        return self.parse(html)
