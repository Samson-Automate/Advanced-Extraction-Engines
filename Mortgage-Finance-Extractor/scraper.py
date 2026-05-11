import time
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# --- GLOBAL CONFIGURATION ---
TARGET_URL = "https://finance.yahoo.com/research-hub/screener/sec-ind_ind-largest-equities_mortgage-finance/"
REQUIRED_COLUMNS = ['Symbol', 'Name', 'Price (Intraday)']

def initialize_driver():
    """
    Configures and initializes a headless Chrome WebDriver.
    Using headless mode improves performance and is standard for scraping scripts.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Custom User-Agent to mimic a real browser and avoid basic bot detection
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    return webdriver.Chrome(options=chrome_options)

def fetch_screener_data(url: str) -> pd.DataFrame:
    """
    Navigates to the Yahoo Finance screener and extracts the dynamic table data.
    """
    driver = initialize_driver()
    try:
        print(f"Initiating request to: {url}")
        driver.get(url)
        
        # Explicit wait for JavaScript-rendered table content to populate
        time.sleep(5) 

        # Utilize BeautifulSoup for robust HTML parsing
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        raw_table = soup.find('table')

        if not raw_table:
            raise RuntimeError("Extraction failed: Could not locate the data table.")

        # StringIO wrapper ensures compatibility with Pandas 2.0+ 
        # and avoids 'FileNotFound' OSError during string parsing
        html_stream = StringIO(str(raw_table))
        df_list = pd.read_html(html_stream)
        
        # Return the primary dataframe found on the page
        return df_list[0]

    finally:
        # Ensure driver process is terminated to free up system resources
        driver.quit()

def process_and_output(df: pd.DataFrame):
    """
    Cleans the dataframe headers and filters for relevant financial metrics.
    """
    # Sanitize column names by removing leading/trailing whitespace
    df.columns = [col.strip() for col in df.columns]
    
    # Dynamically verify if required headers are present in the scraped set
    valid_cols = [c for c in REQUIRED_COLUMNS if c in df.columns]
    
    if valid_cols:
        final_view = df[valid_cols]
        print("\n[SUCCESS] Scraped Mortgage Finance Data:")
        print("-" * 60)
        print(final_view.head(10))
        print("-" * 60)
    else:
        print("\n[WARNING] Expected headers not found. Defaulting to raw data output:")
        print(df.head())

if __name__ == "__main__":
    try:
        # Execute scraping workflow
        raw_data = fetch_screener_data(TARGET_URL)
        
        # Perform data cleaning and display
        process_and_output(raw_data)
        
    except Exception as error:
        print(f"\n[CRITICAL ERROR] Script execution failed: {error}")
