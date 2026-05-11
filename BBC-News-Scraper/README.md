# BBC News Automated Scraper

A robust Python-based web scraping tool designed to extract the latest headlines and articles from the BBC News homepage. This project focuses on data cleaning, handling relative URLs, and filtering out non-news navigation links to provide a structured dataset.

## Core Features
* **Smart Filtering:** Automatically excludes site navigation links (Home, Sport, etc.) and targets actual news articles.
* **URL Normalization:** Converts relative paths into absolute URLs for immediate use.
* **Data Deduplication:** Ensures unique headlines using Pandas.
* **Professional Logging:** Includes execution tracking to monitor scraping success or errors.
* **Object-Oriented Design:** Built using a modular class structure for easy integration into larger projects.

## Technical Stack
* **Python 3.x**
* **BeautifulSoup4:** For HTML parsing.
* **Requests:** For handling HTTP protocols.
* **Pandas:** For data structuring and cleaning.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com
   cd bbc-news-automated-scraper
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Simply run the main script to fetch the latest headlines:

```bash
python bbc_scraper.py
```

To save the data to a CSV file for analysis, uncomment the `to_csv` line in the script's entry point.

## Sample Output
The scraper returns a cleaned and structured DataFrame:


| # | Headline | Link |
|---|---|---|
| 1 | Trump calls Iran response to US proposal... | https://bbc.com... |
| 2 | Thailand's divisive ex-PM is out of jail... | https://bbc.com... |

---
**Disclaimer:** This project is for educational purposes only. Please ensure compliance with the target website's Terms of Service and robots.txt before use.
