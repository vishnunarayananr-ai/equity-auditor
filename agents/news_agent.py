# agents/news_agent.py
# Responsible for ALL news fetching and cleaning
# Single responsibility: NEWS ONLY — no analysis, no UI

import requests
from bs4 import BeautifulSoup

class NewsAgent:
    """
    Scrapes and processes financial news headlines.
    Single responsibility: NEWS FETCHING ONLY.
    """

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        )
    }

    def __init__(self, ticker: str):
        self.ticker = ticker.upper().strip()

    def fetch_google_news(self) -> list:
        """Scrape headlines from Google News search."""
        try:
            url = f"https://www.google.com/search?q={self.ticker}+stock+news&tbm=nws"
            resp = requests.get(url, headers=self.HEADERS, timeout=8)
            soup = BeautifulSoup(resp.text, "html.parser")

            # Try primary selector
            headlines = [
                h.get_text()
                for h in soup.find_all("div", attrs={"class": "vv77bd"})
            ]

            # Fallback selector
            if not headlines:
                headlines = [
                    h.get_text()
                    for h in soup.find_all("div", role="heading")
                ]

            return headlines[:15] if headlines else []
        except Exception:
            return []

    def fetch_rss_news(self) -> list:
        """Fallback — fetch from Google News RSS feed."""
        try:
            url = f"https://news.google.com/rss/search?q={self.ticker}+stock+news"
            resp = requests.get(url, headers=self.HEADERS, timeout=8)
            soup = BeautifulSoup(resp.text, "xml")
            items = soup.find_all("item")[:15]
            return [item.title.text for item in items if item.title]
        except Exception:
            return []

    def clean_headlines(self, headlines: list) -> list:
        """Remove duplicates, empty strings and clean whitespace."""
        seen = set()
        cleaned = []
        for h in headlines:
            h = h.strip()
            if h and h not in seen and len(h) > 10:
                seen.add(h)
                cleaned.append(h)
        return cleaned

    def get_headlines(self) -> list:
        """
        Main method — tries Google News first, falls back to RSS.
        Always returns a clean list of headlines.
        """
        headlines = self.fetch_google_news()

        if not headlines:
            headlines = self.fetch_rss_news()

        headlines = self.clean_headlines(headlines)

        if not headlines:
            headlines = [f"No recent news found for {self.ticker}."]

        return headlines