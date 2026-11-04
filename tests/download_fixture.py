import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

try:
    from parsers.base import fetch_html
    from restaurants import RESTAURANTS, RestaurantConfig
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from parsers.base import fetch_html
    from restaurants import RESTAURANTS, RestaurantConfig

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def slugify_restaurant_id(section_id: str) -> str:
    """Convert a restaurant section_id (e.g. 'Food Garden', 'Šestka') into lowercase ASCII snake_case."""
    normalized = unicodedata.normalize("NFKD", section_id)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "_", ascii_text).strip("_")
    if not slug:
        raise ValueError(
            f"Could not derive a valid filename slug from section_id={section_id!r}."
        )
    return slug


def find_restaurant(
    identifier: str, restaurants: list[RestaurantConfig] = RESTAURANTS
) -> RestaurantConfig:
    """Find a RestaurantConfig in `restaurants.py` by exact section_id (case-insensitive) or slug."""
    target_lower = identifier.strip().lower()
    target_slug = slugify_restaurant_id(identifier)
    for entry in restaurants:
        if (
            entry.section_id.lower() == target_lower
            or slugify_restaurant_id(entry.section_id) == target_slug
        ):
            return entry
    available = ", ".join(
        f"{r.section_id!r} ({slugify_restaurant_id(r.section_id)})" for r in restaurants
    )
    raise KeyError(
        f"Restaurant {identifier!r} not found in restaurants.py. Available: {available}"
    )


def download_restaurant_fixture(
    entry: RestaurantConfig,
    snapshot_date: date | None = None,
    fixtures_dir: Path = FIXTURES_DIR,
    timeout: float = 15.0,
) -> Path:
    """Download raw HTML for `entry` and save it as `tests/fixtures/<slug>_<yyyy_mm_dd>.html`."""
    target_date = snapshot_date or date.today()
    slug = slugify_restaurant_id(entry.section_id)
    filename = f"{slug}_{target_date:%Y_%m_%d}.html"
    output_path = fixtures_dir / filename

    fixtures_dir.mkdir(parents=True, exist_ok=True)
    html = fetch_html(entry.url, timeout=timeout)
    output_path.write_text(html, encoding="utf-8")
    return output_path


def main(argv: list[str] | None = None) -> list[Path]:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Download raw HTML snapshots for restaurants configured in restaurants.py into tests/fixtures/."
    )
    parser.add_argument(
        "restaurants",
        nargs="*",
        help="One or more restaurant section_ids or slugs from restaurants.py (e.g. 'Food Garden' astra).",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Download fixtures for all restaurants listed in restaurants.py.",
    )
    parser.add_argument(
        "--date",
        help="Override snapshot date in YYYY_MM_DD or YYYY-MM-DD format (defaults to today).",
    )
    args = parser.parse_args(argv)

    if not args.all and not args.restaurants:
        parser.error("Provide at least one restaurant section_id/slug or pass --all.")

    snapshot_date: date | None = None
    if args.date:
        normalized_date = args.date.replace("_", "-")
        snapshot_date = date.fromisoformat(normalized_date)

    targets = (
        list(RESTAURANTS)
        if args.all
        else [find_restaurant(name) for name in args.restaurants]
    )

    saved_paths: list[Path] = []
    for entry in targets:
        path = download_restaurant_fixture(entry, snapshot_date=snapshot_date)
        print(f"Saved {entry.section_id} ({entry.url}) -> {path}")
        saved_paths.append(path)

    return saved_paths


if __name__ == "__main__":
    main()
