import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

# Professional Logging setup for tracking script execution
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BBCScraper:
    def __init__(self):
        self.url = "https://bbc.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        self.base_url = "https://bbc.com"

    def fetch_page(self):
        """Downloads HTML content from the target URL."""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to access the website: {e}")
            return None

    def parse_headlines(self, html_content):
        """Parses HTML and extracts relevant news headlines and links."""
        soup = BeautifulSoup(html_content, "html.parser")
        news_items = []
        
        # Find all anchor tags
        articles = soup.find_all("a")
        
        for article in articles:
            headline = article.get_text(strip=True)
            link = article.get("href")

            if headline and link:
                # Filter specifically for news articles and world news
                # This excludes general navigation links like 'Home' or 'Sport'
                if "/news/articles/" in link or "/news/world" in link:
                    # Convert relative links to absolute URLs
                    full_link = link if link.startswith("http") else self.base_url + link
                    
                    news_items.append({
                        "Headline": headline,
                        "Link": full_link
                    })
        
        return news_items

    def get_cleaned_data(self):
        """Executes the full workflow and returns a cleaned DataFrame."""
        html = self.fetch_page()
        if not html:
            return pd.DataFrame()

        raw_data = self.parse_headlines(html)
        df = pd.DataFrame(raw_data)
        
        if not df.empty:
            # Remove duplicate headlines to ensure unique data
            df = df.drop_duplicates(subset=['Headline']).reset_index(drop=True)
            logging.info(f"Successfully scraped {len(df)} headlines.")
        
        return df

if __name__ == "__main__":
    # Initialize and execute the scraper
    scraper = BBCScraper()
    news_df = scraper.get_cleaned_data()

    if not news_df.empty:
        print("\n--- BBC LATEST HEADLINES ---\n")
        print(news_df.head(20))
        
        # Optional: Save results to a CSV file
        # news_df.to_csv("bbc_news.csv", index=False)
    else:
        print("No news data was found.")
