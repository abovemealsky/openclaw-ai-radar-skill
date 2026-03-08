#!/usr/bin/env python3
"""
Fetch research papers from arXiv.
"""
import json
import os
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import feedparser

# Get the skill root directory (parent of scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)

SOURCES_FILE = os.path.join(SKILL_ROOT, "sources/research_sources.json")
OUTPUT_FILE = os.path.join(SKILL_ROOT, "data/raw/research.json")

# Set mode: "daily" (24h) or "weekly" (7 days)
MODE = os.environ.get("RADAR_MODE", "daily")
MAX_AGE_DAYS = 1 if MODE == "daily" else 7


def load_sources():
    """Load arXiv sources from JSON config."""
    with open(SOURCES_FILE, "r") as f:
        data = json.load(f)
    return data.get("sources", [])


def fetch_arxiv_feed(source_url):
    """Fetch arXiv RSS feed."""
    try:
        feed = feedparser.parse(source_url)
        entries = []
        now = datetime.now()
        cutoff_date = now - timedelta(days=MAX_AGE_DAYS)
        
        for entry in feed.entries:
            # Extract published date
            published = ""
            published_dt = None
            
            if hasattr(entry, "published"):
                try:
                    published_dt = date_parser.parse(entry.published)
                    published = published_dt.strftime("%Y-%m-%d")
                except:
                    published = now.strftime("%Y-%m-%d")
            
            # Skip old entries
            if published_dt:
                if published_dt.tzinfo is not None:
                    published_dt = published_dt.replace(tzinfo=None)
                if published_dt < cutoff_date:
                    continue
            
            # Determine category from URL
            source = "arXiv"
            if "cs.AI" in source_url:
                source = "arXiv CS.AI"
            elif "cs.CL" in source_url:
                source = "arXiv CS.CL"
            elif "cs.LG" in source_url:
                source = "arXiv CS.LG"
            
            # Clean title (remove newlines)
            title = entry.get("title", "").replace("\n", " ").strip()
            
            entries.append({
                "title": title,
                "link": entry.get("link", ""),
                "published": published,
                "source": source
            })
        return entries
    except Exception as e:
        print(f"Error fetching {source_url}: {e}")
        return []


def main():
    """Main function to fetch all research papers."""
    os.makedirs(os.path.join(SKILL_ROOT, "data/raw"), exist_ok=True)
    
    sources = load_sources()
    print(f"Fetching research from {len(sources)} sources (mode: {MODE}, max {MAX_AGE_DAYS} days)...")
    
    all_items = []
    for source in sources:
        print(f"Fetching: {source}")
        items = fetch_arxiv_feed(source)
        all_items.extend(items)
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)
    
    if len(all_items) == 0:
        print(f"Note: arXiv typically does not publish on weekends (Saturday-Sunday)")
    
    print(f"Fetched {len(all_items)} research papers -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
