# Yahoo Finance Mortgage Sector Scraper

A Python utility built to solve a specific problem: scraping Yahoo Finance screeners that use heavy JavaScript. Standard libraries like `requests` or `pd.read_html` usually fail on these pages because the data tables are rendered dynamically after the page loads.

This script uses a combination of Selenium (for browser automation) and BeautifulSoup/Pandas (for data extraction) to reliably pull the latest Mortgage Finance stock data.

## Why I built this
Yahoo Finance's research hub is a great resource, but it's difficult to automate data collection from it. The tables aren't in the static HTML source. I wrote this to:
- Automate the "waiting" process for dynamic content.
- Handle common parsing errors (like the `OSError` and `lxml` issues typical with messy web HTML).
- Provide a clean, structured DataFrame for financial analysis.

## The Approach
- **Selenium (Headless):** Used to launch a background browser that executes the JavaScript required to populate the tables.
- **BeautifulSoup:** Acts as a middleman to "clean" the raw page source before passing it to Pandas.
- **Pandas & StringIO:** Final data processing to extract specific columns like Symbol, Name, and Intraday Price.

## Setup
You'll need Python 3.x and Chrome installed on your machine.

### 1. Clone the repo
```bash
git clone https://github.com
cd your-repo-name
```

### 2. Install dependencies
```bash
pip install pandas selenium beautifulsoup4 lxml
```

### 3. Run the script
```bash
python yahoo_scraper.py
```

## A note on the code
I've refactored the script into modular functions (initialization, fetching, and cleaning) rather than one long script. This makes it easier to maintain and update if Yahoo changes their CSS classes or table structure. 

The script currently filters for:
- **Symbol**
- **Name**
- **Price (Intraday)**

## Troubleshooting
If you run into issues with the Chrome driver, ensure your Chrome browser is up to date. The script is configured to run "headless" (without a visible window) to save resources, but you can disable this in `initialize_driver()` if you want to watch the scraping happen.


