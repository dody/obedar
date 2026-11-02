from abc import ABC, abstractmethod
from urllib.parse import urldefrag
from urllib.request import Request, urlopen

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "sk-SK,sk;q=0.9,en;q=0.8",
}


def fetch_html(url: str, timeout: float = 15.0) -> str:
    """Download raw HTML from `url` and decode it using the response charset (default UTF-8)."""
    clean_url = urldefrag(url).url
    request = Request(clean_url, headers=DEFAULT_HEADERS)
    with urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


class RestaurantParser(ABC):
    """Base interface for restaurant daily menu parsers."""

    name: str
    url: str

    def fetch_html(self, timeout: float = 15.0) -> str:
        return fetch_html(self.url, timeout=timeout)

    @abstractmethod
    def parse(self, html: str) -> list[str]:
        """Parse raw HTML and return the menu as a simple list of lines."""

    def get_menu(self, timeout: float = 15.0) -> list[str]:
        """Fetch the restaurant page and return the parsed list of menu lines."""
        html = self.fetch_html(timeout=timeout)
        return self.parse(html)

