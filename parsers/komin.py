import re

from parsers.sme import SmeParser

_DATE_ONLY_RE = re.compile(r"^\d{1,2}\.\d{1,2}\.\d{4}$")


class KominParser(SmeParser):
    """Daily menu parser for Ružinovský pivovar Komín (hosted on restauracie.sme.sk)."""

    def parse(self, html: str) -> list[str]:
        raw_lines = super().parse(html)
        return [line for line in raw_lines if not _DATE_ONLY_RE.match(line.strip())]


def parse_komin_menu(html: str) -> list[str]:
    """Parse raw Komín (restauracie.sme.sk) HTML into a list of menu lines."""
    return KominParser().parse(html)
