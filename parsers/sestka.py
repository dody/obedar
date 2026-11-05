from parsers.sme import SmeParser

_SLOVAK_DAYS = {
    "pondelok",
    "utorok",
    "streda",
    "štvrtok",
    "piatok",
    "sobota",
    "nedeľa",
}

_ENGLISH_DAYS = {
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
}


class SestkaParser(SmeParser):
    """Daily menu parser for Šestka Canteen (hosted on restauracie.sme.sk)."""

    def parse(self, html: str) -> list[str]:
        raw_lines = super().parse(html)
        filtered: list[str] = []
        for line in raw_lines:
            lowered = line.strip().lower()
            if lowered in _ENGLISH_DAYS:
                break
            if lowered in _SLOVAK_DAYS:
                continue
            filtered.append(line)
        return filtered


def parse_sestka_menu(html: str) -> list[str]:
    """Parse raw Šestka (restauracie.sme.sk) HTML into a list of menu lines."""
    return SestkaParser().parse(html)
