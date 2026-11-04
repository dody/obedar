# Obedár — Agent Workflow & Project Rules

This repository scrapes daily lunch menus from configured restaurants and builds a JSON payload for an email notification service.

## Architecture Overview

- **`restaurants.py`** — Single source of truth for restaurant configurations (`RESTAURANTS: list[RestaurantConfig]`) and `AUTHOR`. Each entry maps:
  - `section_id`: Display/service ID of the restaurant (can contain spaces and Slovak diacritics, e.g. `"Food Garden"`, `"Šestka"`, `"Pizzeria Rotunda"`).
  - `url`: URL of the restaurant's daily menu page.
  - `parser`: `RestaurantParser` subclass used to parse the page (can be `None` temporarily while bootstrapping a new restaurant before its parser is implemented).
- **`parsers/`** — `BeautifulSoup` (`from bs4 import BeautifulSoup`) menu parsers inheriting from `RestaurantParser` (`parsers/base.py`).
- **`tests/fixtures/`** — Real, unmodified HTML snapshots downloaded from restaurant URLs, named `<slug>_<yyyy_mm_dd>.html` (where `<slug>` is the lowercase ASCII `snake_case` of `section_id`, e.g. `food_garden_2026_11_04.html`, `astra_2026_11_04.html`).
- **`tests/download_fixture.py`** — Helper script that reads `restaurants.py`, fetches the live HTML for a restaurant, and writes it to `tests/fixtures/<slug>_<yyyy_mm_dd>.html`.
- **`main.py`** — Builds and prints the final JSON payload (`{"author": ..., "sections": [{"section_id": ..., "menu": [...]}]}`).

---

## Mandatory Workflow for Adding or Updating a Restaurant Parser

**Never embed synthetic or hand-copied HTML strings inside new test files.** Always test against real HTML snapshots saved in `tests/fixtures/`.

When asked to add a new restaurant (or update an existing parser), follow these steps in order:

### Step 1: Register the Restaurant in `restaurants.py`

Add a `RestaurantConfig` entry to `RESTAURANTS` in `restaurants.py` with the restaurant's `section_id` and `url` (you may leave `parser=None` until Step 4 if the parser class does not exist yet):

```python
RestaurantConfig(
    section_id="Pizzeria Rotunda",
    url="https://...",
    parser=None,
),
```

### Step 2: Download the Real HTML Snapshot into `tests/fixtures/`

Run the fixture downloader using the restaurant's `section_id` (or slug):

```powershell
python -m tests.download_fixture "Pizzeria Rotunda"
```

This fetches the live HTML using `parsers.base.fetch_html` and saves it unmodified to:
`tests/fixtures/<slug>_<yyyy_mm_dd>.html` (e.g., `tests/fixtures/pizzeria_rotunda_2026_11_04.html`).

Inspect the saved HTML file in `tests/fixtures/` to locate the exact DOM structure for the daily menu.

### Step 3: Write the Test First (`tests/test_<slug>.py`)

Create or update the unit test in `tests/test_<slug>.py` so it loads the downloaded HTML file from `tests/fixtures/<slug>_<yyyy_mm_dd>.html` and asserts the exact expected `list[str]` of menu lines:

```python
from pathlib import Path
import unittest

from parsers.rotunda import parse_rotunda_menu

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class RotundaParserTests(unittest.TestCase):
    def test_parses_pizzeria_rotunda_fixture(self) -> None:
        html = (FIXTURES_DIR / "pizzeria_rotunda_2026_11_04.html").read_text(encoding="utf-8")
        result = parse_rotunda_menu(html)
        self.assertEqual(
            result,
            [
                # Expected menu lines confirmed with the user or from the fixture
            ],
        )
```

### Step 4: Implement the Parser (`parsers/<slug>.py`) & Wire `restaurants.py`

1. Implement the parser class in `parsers/<slug>.py` inheriting from `RestaurantParser` and using `from bs4 import BeautifulSoup`. Do not add unused exports in `parsers/__init__.py` or unused helper functions.
2. Set `parser=<NewParserClass>` on the restaurant's `RestaurantConfig` entry in `restaurants.py`.

### Step 5: Verify with Unit Tests and `main.py`

1. Run the test suite:

   ```powershell
   python -m unittest discover -s tests
   ```

2. Run the end-to-end payload builder:

   ```powershell
   python main.py
   ```
