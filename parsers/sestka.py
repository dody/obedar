from parsers.sme import SmeParser, parse_sme_menu


class SestkaParser(SmeParser):
    """Daily menu parser for Šestka Canteen (hosted on restauracie.sme.sk)."""


def parse_sestka_menu(html: str) -> list[str]:
    """Parse raw Šestka (restauracie.sme.sk) HTML into a list of menu lines."""
    return SestkaParser().parse(html)
