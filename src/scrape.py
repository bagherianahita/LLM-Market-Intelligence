"""Web/news scraping for market intelligence pipeline."""

import argparse

import requests
from bs4 import BeautifulSoup


def scrape_url(url: str) -> str:
    """Scrape paragraph text from a press release or news page."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return " ".join(p.get_text() for p in soup.find_all("p"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()
    print(scrape_url(args.url)[:500])
