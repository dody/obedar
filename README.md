# Obedár

Daily lunch menu scraper for configured restaurants that outputs a structured JSON payload (and optionally pushes it to a configured webhook/Google Sheets endpoint via `API_URL`).

## Setup & Installation

Create and activate a virtual environment using `venv`, then install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Or install BeautifulSoup directly:

```bash
pip install beautifulsoup4 requests
```

## Usage

Run the scraper to fetch daily menus and print the JSON payload:

```bash
python main.py
```

If an `API_URL` is configured via environment variable or a local `.env` file (`API_URL=https://...`), `main.py` will also POST the JSON payload to that URL.

## Running Tests

Run the unit test suite against the HTML fixtures in `tests/fixtures/`:

```bash
python -m unittest discover -s tests
```

To download a fresh HTML fixture for a configured restaurant:

```bash
python -m tests.download_fixture "Food Garden"
```

## Cron Schedule

To automatically update the repository and run the scraper every workday (Monday–Friday) at 10:00 AM via [run.sh](run.sh), add the following entry with `crontab -e`:

```cron
0 10 * * 1-5 <projects dir>/obedar/run.sh >> <projects dir>/obedar/cron.log
```
