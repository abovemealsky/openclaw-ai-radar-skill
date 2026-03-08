#!/usr/bin/env python3
"""
Fetch AI news from RSS sources.
"""
import json
import os
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import feedparser

# Get the skill root directory (parent of scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)

SOURCES_FILE = os.path.join(SKILL_ROOT, "sources/news_sources.json")
OUTPUT_FILE = os.path.join(SKILL_ROOT, "data/raw/news.json")

# Only keep news from the last 7 days
MAX_AGE_DAYS = 7


def load_sources():
    """Load news sources from JSON config."""
    with open(SOURCES_FILE, "r") as f:
        data = json.load(f)
    return data.get("sources", [])


def fetch_feed(source_url):
    """Fetch a single RSS feed."""
    try:
        feed = feedparser.parse(source_url)
        entries = []
        now = datetime.now()
        cutoff_date = now - timedelta(days=MAX_AGE_DAYS)
        
        for entry in feed.entries:
            # Try to extract published date
            published = ""
            published_dt = None
            
            if hasattr(entry, "published"):
                try:
                    published_dt = date_parser.parse(entry.published)
                    published = published_dt.strftime("%Y-%m-%d")
                except:
                    published = now.strftime("%Y-%m-%d")
            elif hasattr(entry, "updated"):
                try:
                    published_dt = date_parser.parse(entry.updated)
                    published = published_dt.strftime("%Y-%m-%d")
                except:
                    published = now.strftime("%Y-%m-%d")
            
            # Skip old entries (handle timezone-aware dates)
            if published_dt:
                # Convert to naive datetime for comparison
                if published_dt.tzinfo is not None:
                    published_dt = published_dt.replace(tzinfo=None)
                if published_dt < cutoff_date:
                    continue
            
            # Extract source name from feed or URL
            source = feed.feed.get("title", source_url)
            if "openai" in source_url.lower():
                source = "OpenAI"
            elif "anthropic" in source_url.lower():
                source = "Anthropic"
            elif "google" in source_url.lower():
                source = "Google AI"
            
            entries.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": published,
                "source": source
            })
        return entries
    except Exception as e:
        print(f"Error fetching {source_url}: {e}")
        return []


def main():
    """Main function to fetch all news."""
    # Ensure output directory exists
    os.makedirs("data/raw", exist_ok=True)
    
    sources = load_sources()
    print(f"Fetching news from {len(sources)} sources...")
    
    all_items = []
    for source in sources:
        print(f"Fetching: {source}")
        items = fetch_feed(source)
        all_items.extend(items)
    
    # Save to JSON
    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)
    
    print(f"Fetched {len(all_items)} news items -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
